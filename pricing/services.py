# pricing/services.py
from django.utils import timezone
from products.models import Product
from .models import PriceSuggestion, LogisticsInfo
from .utils import suggest_price, estimate_logistics

def generate_pricing_and_logistics(product: Product):
    ps = suggest_price(product)
    PriceSuggestion.objects.create(
        product=product,
        suggested_price=ps.price,
        rationale=ps.rationale,
        created_at=timezone.now()
    )
    lg = estimate_logistics(product)
    LogisticsInfo.objects.create(
        product=product,
        region=lg.region,
        carrier=lg.carrier,
        estimated_days=lg.days,
        cost_estimate=lg.cost
    )
