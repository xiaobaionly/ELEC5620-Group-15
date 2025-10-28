from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from products.views import (
    home, seller_dashboard, buyer_catalog,
    product_detail, product_create, product_edit, generate_desc,
    product_toggle_active
)
from accounts.views import register, role_route, logout_get, seller_profile  # Key import

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),

    # Home page
    path('', home, name='home'),

    # Account management
    path('accounts/register/', register, name='register'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', logout_get, name='logout'),
    path('accounts/route/', role_route, name='role-route'),

    # Seller section
    path('seller/', seller_dashboard, name='seller-dashboard'),
    path('seller/profile/', seller_profile, name='seller-profile'),
    path('seller/products/<int:pk>/toggle/', product_toggle_active, name='product-toggle'),
    path('seller/products/new/', product_create, name='product-create'),
    path('seller/products/<int:pk>/edit/', product_edit, name='product-edit'),
    path('seller/products/<int:pk>/gen-desc/', generate_desc, name='product-gen-desc'),

    # Buyer section
    path('buy/', buyer_catalog, name='buyer-catalog'),
    path('buy/products/<int:pk>/', product_detail, name='product-detail'),
]

# Serve media files in development mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
