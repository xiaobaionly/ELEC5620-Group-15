from django.contrib import admin
from .models import SupplierProfile, Product
admin.site.register(SupplierProfile)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id","name","category","stock","base_price","supplier")
