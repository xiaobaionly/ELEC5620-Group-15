from django.contrib.auth.models import AbstractUser
from django.db import models

# Import the concrete SupplierProfile to create a proxy model in this app
from products.models import SupplierProfile


class User(AbstractUser):
    """
    Custom user with a simple role field.
    """
    class Role(models.TextChoices):
        SELLER = "SELLER", "Seller"
        BUYER = "BUYER", "Buyer"

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.BUYER)

    def is_seller(self) -> bool:
        return self.role == self.Role.SELLER

    def is_buyer(self) -> bool:
        return self.role == self.Role.BUYER


class SupplierProfileProxy(SupplierProfile):
    """
    Proxy model so SupplierProfile appears under the 'Accounts' app section in Django Admin.
    No database table is created or altered.
    """
    class Meta:
        proxy = True
        verbose_name = "Supplier profile"
        verbose_name_plural = "Supplier profiles"
