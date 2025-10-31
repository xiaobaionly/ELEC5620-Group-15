from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from .models import SupplierProfileProxy

User = get_user_model()

# Hide the built-in Groups from the sidebar
try:
    admin.site.unregister(Group)
except Exception:
    pass

# Unregister default User admin first
try:
    admin.site.unregister(User)
except Exception:
    pass


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Custom User admin with a visible role column ('Seller' / 'Buyer').
    """
    search_fields = ("id", "username", "email", "first_name", "last_name")
    list_display = ("id", "username", "email", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_superuser", "is_active")
    ordering = ("id",)

    # Optional: extend fieldsets to include role in the user edit form
    fieldsets = BaseUserAdmin.fieldsets + (
        ("User Role", {"fields": ("role",)}),
    )


@admin.register(SupplierProfileProxy)
class SupplierProfileProxyAdmin(admin.ModelAdmin):
    """
    Display Supplier profiles under the 'Accounts' section using a proxy model.
    """
    list_display = ("id", "user", "company_name", "contact_name", "phone", "email")
    search_fields = ("id", "user__username", "company_name", "contact_name", "phone", "email")
    list_filter = ("company_name",)
    ordering = ("id",)

from django.contrib import admin

# === Custom Admin Branding ===
admin.site.site_header = "AgriMate Administration"
admin.site.site_title = "AgriMate Admin Portal"
admin.site.index_title = "Welcome to AgriMate Control Panel"