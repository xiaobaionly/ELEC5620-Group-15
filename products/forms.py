# products/forms.py
from django import forms
from .models import Product, SupplierProfile


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'unit', 'stock', 'base_price', 'image', 'purchase_link']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'name': 'Product name (required)',
            'category': 'e.g. Vegetable / Fruit / Grain',
            'unit': 'kg / box / bag',
            'stock': 'Stock quantity',
            'base_price': 'Base price (excluding shipping)',
            'purchase_link': 'https://example.com/product',
        }
        for name, field in self.fields.items():
            if hasattr(field.widget, 'attrs'):
                cls = (
                    'w-full rounded-lg border px-3 py-2 '
                    'focus:outline-none focus:ring-2 focus:ring-green-500'
                )
                field.widget.attrs['class'] = cls
                if name in placeholders:
                    field.widget.attrs.setdefault('placeholder', placeholders[name])
        self.fields['stock'].widget.attrs['min'] = 0
        self.fields['base_price'].widget.attrs['step'] = '0.01'


# ==== Key modification: generic, not tied to specific field names ====
class SupplierProfileForm(forms.ModelForm):
    class Meta:
        model = SupplierProfile
        # Include all model fields except system-managed ones
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Remove system fields that should not be user-editable
        for n in ('user', 'id', 'created_time', 'updated_time'):
            if n in self.fields:
                self.fields.pop(n)

        # Apply consistent Tailwind CSS styling (only if field exists)
        for name, field in self.fields.items():
            if hasattr(field.widget, 'attrs'):
                field.widget.attrs.setdefault(
                    'class',
                    'w-full rounded-lg border px-3 py-2 '
                    'focus:outline-none focus:ring-2 focus:ring-green-500'
                )

        # Common field optimizations (only if field exists)
        if 'description' in self.fields:
            self.fields['description'].widget = forms.Textarea(
                attrs={
                    'rows': 4,
                    'class': 'w-full rounded-lg border px-3 py-2 '
                             'focus:outline-none focus:ring-2 focus:ring-green-500'
                }
            )
        if 'phone' in self.fields:
            self.fields['phone'].widget.attrs.setdefault('placeholder', 'Contact phone')
        if 'company_name' in self.fields:
            self.fields['company_name'].widget.attrs.setdefault('placeholder', 'Company name (required)')
