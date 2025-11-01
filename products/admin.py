from django.contrib import admin
from .models import Product



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin for Product.
    Hides the 'Supplier' column, keeps 'User' (owner) for clarity.
    """

    list_display = (
        "id",
        "name",
        "category",
        "unit",
        "stock",
        "base_price",
        "owner",       # user who owns the supplier
        "is_active",
        "created_at",
    )

    # Allow searching by product info or supplier-related fields
    search_fields = (
        "id",
        "name",
        "category",
        "supplier__company_name",
        "supplier__contact_name",
        "supplier__user__username",
        "supplier__user__email",
    )

    # Filters for category, active status, and supplier's user
    list_filter = ("category", "is_active", ("supplier__user", admin.RelatedOnlyFieldListFilter))

    # Optimize queries (only load supplier->user, no need to prefetch supplier itself)
    list_select_related = ("supplier__user",)

    ordering = ("-created_at",)
    readonly_fields = ("created_at",)

    def owner(self, obj):
        """Return the auth user behind this product's supplier."""
        return getattr(obj.supplier, "user", None)

    owner.short_description = "User"
    owner.admin_order_field = "supplier__user"
