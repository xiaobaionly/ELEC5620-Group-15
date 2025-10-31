from django.contrib import admin
from .models import Product

# Do NOT register SupplierProfile here anymore – it is exposed via the proxy in Accounts.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin for Product.
    Adds 'owner' column showing the auth user behind the supplier.
    """
    list_display = (
        "id",
        "name",
        "category",
        "unit",
        "stock",
        "base_price",
        "supplier",
        "owner",      # user who owns the supplier
        "is_active",
        "created_at",
    )

    # Search also by supplier's user (creator/owner)
    search_fields = (
        "id",
        "name",
        "category",
        "supplier__company_name",
        "supplier__contact_name",
        "supplier__user__username",
        "supplier__user__email",
    )

    # Filter by category/active and by owner user
    list_filter = ("category", "is_active", ("supplier__user", admin.RelatedOnlyFieldListFilter))

    # Speed up joins in changelist
    list_select_related = ("supplier", "supplier__user")

    ordering = ("-created_at",)
    readonly_fields = ("created_at",)

    def owner(self, obj):
        """Return the auth user behind this product's supplier."""
        return getattr(obj.supplier, "user", None)

    owner.short_description = "User"
    owner.admin_order_field = "supplier__user"
