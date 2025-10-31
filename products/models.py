from django.db import models
from django.conf import settings


class SupplierProfile(models.Model):
    """
    Supplier profile linked 1:1 to the auth user.
    Provides business identity and basic contact info for suppliers.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200)
    contact_name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    address = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to="logos/", blank=True, null=True)
    business_license = models.FileField(upload_to="licenses/", blank=True, null=True)

    class Meta:
        verbose_name = "Supplier profile"
        verbose_name_plural = "Supplier profiles"
        # Friendly default ordering in admin lists
        ordering = ["company_name", "id"]

    def __str__(self) -> str:
        """Human-readable identifier in admin and foreign key dropdowns."""
        return self.company_name or f"Supplier #{self.pk} ({self.user})"


class Product(models.Model):
    """
    A product listed by a supplier, with basic inventory and pricing fields.
    """
    supplier = models.ForeignKey(SupplierProfile, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100, blank=True)
    unit = models.CharField(max_length=50, default="kg")
    stock = models.PositiveIntegerField(default=0)
    base_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ai_description_en = models.TextField(blank=True)
    ai_description_zh = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name="Active (listed)")

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        # Show newest first in admin lists
        ordering = ["-created_at", "id"]
        # Helpful indexes for common filters/searches (will create a migration)
        indexes = [
            models.Index(fields=["supplier"]),
            models.Index(fields=["name"]),
            models.Index(fields=["category"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self) -> str:
        """Human-readable product name in admin and foreign key dropdowns."""
        return self.name
