from django.db import models
from django.conf import settings
from products.models import Product


class QAThread(models.Model):
    """
    A Q&A thread for a specific product and (optionally) a buyer.
    """
    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    product = models.ForeignKey(
        Product,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Display newest threads first in admin lists
        ordering = ["-created_at"]
        verbose_name = "QA thread"
        verbose_name_plural = "QA threads"

    def __str__(self) -> str:
        buyer_name = getattr(self.buyer, "username", "anonymous")
        product_name = getattr(self.product, "name", "No product")
        return f"{product_name} | {buyer_name} (#{self.pk})"


class QAMessage(models.Model):
    """
    A single message inside a thread.
    """
    thread = models.ForeignKey(
        QAThread,
        on_delete=models.CASCADE,
        related_name="messages",
    )
    sender = models.CharField(
        max_length=10,
        choices=[("BUYER", "BUYER"), ("AI", "AI"), ("SELLER", "SELLER")],
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Show messages chronologically inside a thread
        ordering = ["created_at"]
        verbose_name = "QA message"
        verbose_name_plural = "QA messages"

    def __str__(self) -> str:
        snippet = (self.content[:30] + "…") if self.content and len(self.content) > 30 else self.content
        return f"{self.sender}: {snippet}"
