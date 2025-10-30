# products/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, Http404

from .models import Product, SupplierProfile
from .forms import ProductForm
from ai.llm import LLMClient
from qa.forms import QuestionForm
from pricing.services import generate_pricing_and_logistics
from django.utils.text import Truncator


@login_required
def product_toggle_active(request, pk):
    """Activate/Deactivate toggle (seller only)"""
    if not request.user.is_seller():
        return render(request, "errors/forbidden.html", status=403)
    sp, _ = SupplierProfile.objects.get_or_create(user=request.user)
    product = get_object_or_404(Product, pk=pk, supplier=sp)
    product.is_active = not product.is_active
    product.save(update_fields=["is_active"])
    return redirect("seller-dashboard")


def home(request):
    return render(request, "home.html")


@login_required
def seller_dashboard(request):
    """Seller's own product list"""
    if not request.user.is_seller():
        return render(request, "errors/forbidden.html", status=403)
    sp, _ = SupplierProfile.objects.get_or_create(user=request.user)
    products = Product.objects.filter(supplier=sp).order_by("-created_at")
    return render(request, "seller/dashboard.html", {"products": products})


@login_required
def product_create(request):
    """Create a new product (seller only)"""
    if not request.user.is_seller():
        return render(request, "errors/forbidden.html", status=403)
    sp, _ = SupplierProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            p = form.save(commit=False)
            p.supplier = sp
            p.save()
            return redirect("seller-dashboard")
    else:
        form = ProductForm()
    return render(request, "seller/product_form.html", {"form": form, "title": "Create Product"})


@login_required
def product_edit(request, pk):
    """Edit an existing product (seller only)"""
    if not request.user.is_seller():
        return render(request, "errors/forbidden.html", status=403)
    sp, _ = SupplierProfile.objects.get_or_create(user=request.user)
    p = get_object_or_404(Product, pk=pk, supplier=sp)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=p)
        if form.is_valid():
            form.save()
            return redirect("seller-dashboard")
    else:
        form = ProductForm(instance=p)
    return render(request, "seller/product_form.html", {"form": form, "title": "Edit Product"})


@login_required
def generate_desc(request, pk):
    """One-click generation of English/Chinese descriptions + pricing and logistics suggestions"""
    if not request.user.is_seller():
        return render(request, "errors/forbidden.html", status=403)
    sp, _ = SupplierProfile.objects.get_or_create(user=request.user)
    p = get_object_or_404(Product, pk=pk, supplier=sp)

    llm = LLMClient()
    p.ai_description_en = llm.generate_product_desc(p.name, p.category, p.unit, p.stock, lang="en")
    p.ai_description_zh = llm.generate_product_desc(p.name, p.category, p.unit, p.stock, lang="zh")
    p.save(update_fields=["ai_description_en", "ai_description_zh"])

    generate_pricing_and_logistics(p)
    return redirect("seller-dashboard")


def buyer_catalog(request):
    """Buyer catalog: only show active products"""
    products = Product.objects.filter(is_active=True).order_by("-created_at")
    return render(request, "buyer/catalog.html", {"products": products})


def product_detail(request, pk):
    """
    Buyer product detail view.
    Includes supplier contact info and shipping data for AI question context.
    """
    # Retrieve product and supplier together
    p = get_object_or_404(Product.objects.select_related("supplier"), pk=pk)
    if not p.is_active:
        raise Http404("Product is inactive")

    # Build product context for AI
    unit = p.unit or "kg"

    # Supplier information
    sp = getattr(p, "supplier", None)
    seller_bits = []
    if sp:
        if sp.company_name:
            seller_bits.append(f"Company: {sp.company_name}")
        if sp.contact_name:
            seller_bits.append(f"Contact name: {sp.contact_name}")
        if sp.email:
            seller_bits.append(f"Email: {sp.email}")
        if sp.phone:
            seller_bits.append(f"Phone: {sp.phone}")
        if sp.address:
            seller_bits.append(f"Address: {sp.address}")
    seller_info = "Seller info: " + ("; ".join(seller_bits) if seller_bits else "Not provided")

    # Latest logistics info (if exists)
    lg_last = p.logistics.last() if hasattr(p, "logistics") else None
    logistics_info = ""
    if lg_last:
        logistics_info = (
            f"Shipping: region {lg_last.region}, carrier {lg_last.carrier}, "
            f"ETA approx. {lg_last.estimated_days} days, cost ${lg_last.cost_estimate}"
        )

    # Combine all context text
    ctx_parts = [
        f"Product: {p.name}",
        f"Base price: {p.base_price} per {unit}",
        f"Stock: {p.stock} {unit}",
        f"Category: {p.category}" if p.category else "",
        f"Description (English): {p.ai_description_en or ''}",
        f"Description (Chinese): {p.ai_description_zh or ''}",
        seller_info,
        logistics_info,
    ]
    product_context = "\n".join([x for x in ctx_parts if x])
    product_context = Truncator(product_context).chars(3500)

    # Handle AI question
    ai_answer = None
    form = QuestionForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        q = form.cleaned_data["question"]
        ai = LLMClient()
        ai_answer = ai.answer_question(q, product_context)

    # Render page
    return render(
        request,
        "buyer/product_detail.html",
        {"p": p, "form": form, "ai_answer": ai_answer},
    )


@login_required
def product_delete(request, pk):
   
    if not request.user.is_seller():
        return render(request, "errors/forbidden.html", status=403)
    sp, _ = SupplierProfile.objects.get_or_create(user=request.user)
    p = get_object_or_404(Product, pk=pk, supplier=sp)
    if request.method == "POST":
        p.delete()
        return redirect("seller-dashboard")
    return render(request, "seller/confirm_delete.html", {"product": p})