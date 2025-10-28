# pricing/utils.py
from dataclasses import dataclass
from products.models import Product

@dataclass
class PriceSuggestionResult:
    price: float
    rationale: str


@dataclass
class LogisticsInfoResult:
    region: str
    carrier: str
    days: int
    cost: float


def suggest_price(product: Product) -> PriceSuggestionResult:
    """
    Simple rule: adjust the seller’s base price slightly based on stock, category, and seasonal factors.
    Can be replaced with AI-generated or real market data in the future.
    """
    base = float(product.base_price)
    stock = product.stock

    # The higher the stock, the lower the price; the lower the stock, the higher the price
    inv_factor = 0.95 if stock > 500 else (0.98 if stock > 100 else (1.02 if stock < 30 else 1.0))

    # Category-based adjustment (example)
    cat = (product.category or "").lower()
    cat_factor = 1.00
    if "fruit" in cat:
        cat_factor = 1.05
    elif "vegetable" in cat:
        cat_factor = 0.98

    price = round(base * inv_factor * cat_factor, 2)
    rationale = f"Estimated based on base price {base}, stock {stock}, and category '{product.category}'."
    return PriceSuggestionResult(price=price, rationale=rationale)


def estimate_logistics(product: Product) -> LogisticsInfoResult:
    """
    Logistics estimation: simplified assumption that each item equals one unit of weight and is delivered locally.
    """
    carrier = "AusPost"
    region = "Australia (NSW)"
    # Approximate shipping cost using price as a proxy for weight/volume; replace with actual weight/volume fields if available
    base = float(product.base_price)
    cost = round(max(5.0, min(50.0, base * 0.12)), 2)
    days = 3 if base < 50 else 5
    return LogisticsInfoResult(region=region, carrier=carrier, days=days, cost=cost)
