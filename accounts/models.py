from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        SELLER = "SELLER", "Seller"
        BUYER  = "BUYER",  "Buyer"
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.BUYER)
    def is_seller(self): return self.role == self.Role.SELLER
    def is_buyer(self):  return self.role == self.Role.BUYER
