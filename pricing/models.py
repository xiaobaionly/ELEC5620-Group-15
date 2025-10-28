from django.db import models
from products.models import Product

class PriceSuggestion(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='price_suggestions')
    suggested_price = models.DecimalField(max_digits=10, decimal_places=2)
    rationale = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class LogisticsInfo(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='logistics')
    region = models.CharField(max_length=100)
    carrier = models.CharField(max_length=100, blank=True)
    estimated_days = models.PositiveIntegerField(default=7)
    cost_estimate = models.DecimalField(max_digits=10, decimal_places=2, default=0)
