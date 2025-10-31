from django.db import models
from products.models import Product


class PriceSuggestion(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="price_suggestions")
    suggested_price = models.DecimalField(max_digits=10, decimal_places=2)
    rationale = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Price suggestion"
        verbose_name_plural = "Price suggestions"

    def __str__(self):
        return f"{self.product} → {self.suggested_price}"


class LogisticsInfo(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="logistics")
    region = models.CharField(max_length=100)
    carrier = models.CharField(max_length=100, blank=True)
    estimated_days = models.PositiveIntegerField(default=7)
    cost_estimate = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        ordering = ["product", "region"]
        verbose_name = "Logistics info"
        verbose_name_plural = "Logistics infos"
        indexes = [
            models.Index(fields=["product"]),
            models.Index(fields=["region"]),
        ]

    def __str__(self):
        carrier_part = f" | {self.carrier}" if self.carrier else ""
        return f"{self.product} @ {self.region}{carrier_part} — {self.cost_estimate}"
