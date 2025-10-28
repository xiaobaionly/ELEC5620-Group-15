from django.db import models
from django.conf import settings
from products.models import Product

class QAThread(models.Model):
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

class QAMessage(models.Model):
    thread = models.ForeignKey(QAThread, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=10, choices=[('BUYER','BUYER'),('AI','AI'),('SELLER','SELLER')])
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
