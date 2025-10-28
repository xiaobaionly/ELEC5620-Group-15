# accounts/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseForbidden

from .forms import RegisterForm
from .models import User
from products.models import SupplierProfile
from products.forms import SupplierProfileForm


def register(request):
    """User registration view"""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('role-route')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def role_route(request):
    """Redirect user to the corresponding page based on role"""
    user: User = request.user
    if user.is_seller():
        return redirect('seller-dashboard')
    return redirect('buyer-catalog')


@require_http_methods(["GET"])
def logout_get(request):
    """Logout view (GET request only)"""
    logout(request)
    return redirect('/')  # or redirect('home')


@login_required
def seller_profile(request):
    """Seller profile management page: all editable fields are allowed to be modified"""
    if not request.user.is_seller():
        return HttpResponseForbidden("Only sellers are allowed.")

    sp, _ = SupplierProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = SupplierProfileForm(request.POST, request.FILES, instance=sp)
        if form.is_valid():
            form.save()
            return redirect('seller-profile')
    else:
        form = SupplierProfileForm(instance=sp)

    # Context data passed to the template
    context = {
        'form': form,
        # Used for displaying account info at the top of the page
        'account_username': request.user.get_username(),
        'account_email': getattr(request.user, 'email', ''),
        # Fields already rendered manually in the template (to avoid duplication)
        'placed_fields': [
            'company_name', 'contact_name', 'phone', 'email',
            'address', 'description', 'logo', 'business_license'
        ],
    }
    return render(request, 'seller/profile.html', context)
