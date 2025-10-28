# products/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, Http404

from .models import Product, SupplierProfile
from .forms import ProductForm
from ai.llm import LLMClient
from qa.forms import QuestionForm
from pricing.services import generate_pricing_and_logistics


@login_required
def product_toggle_active(request, pk):
    """Activate/Deactivate toggle (seller only)"""
    if not request.user.is_seller():
        return HttpResponseForbidden("Only sellers allowed.")
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
        return HttpResponseForbidden("Only sellers allowed.")
    sp, _ = SupplierProfile.objects.get_or_create(user=request.user)
    products = Product.objects.filter(supplier=sp).order_by("-created_at")
    return render(request, "seller/dashboard.html", {"products": products})


@login_required
def product_create(request):
    """Create a new product (seller only)"""
    if not request.user.is_seller():
        return HttpResponseForbidden("Only sellers allowed.")
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
        return HttpResponseForbidden("Only sellers allowed.")
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
        return HttpResponseForbidden("Only sellers allowed.")
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
    """Buyer product detail: inactive products are not accessible"""
    p = get_object_or_404(Product, pk=pk)
    if not p.is_active:
        # If you want sellers to still view inactive products, change to:
        # if not (request.user.is_authenticated and request.user.is_seller()):
        raise Http404("Product is inactive")

    ai_answer = None
    form = QuestionForm()
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            q = form.cleaned_data["question"]
            context = (
                f"name={p.name}, price={p.base_price}/{p.unit}, stock={p.stock}, "
                f"supplier={p.supplier.company_name if p.supplier_id else ''}"
            )
            ai = LLMClient()
            ai_answer = ai.answer_question(q, context)

    return render(request, "buyer/product_detail.html", {"p": p, "form": form, "ai_answer": ai_answer})
