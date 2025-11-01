# pricing/management/commands/regen_suggestions.py
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from products.models import Product
from pricing.models import PriceSuggestion, LogisticsInfo
from pricing.services import generate_pricing_and_logistics

class Command(BaseCommand):
    help = "Regenerate price & logistics suggestions for products."

    def add_arguments(self, parser):
        parser.add_argument(
            "--product-id",
            type=int,
            help="Regenerate for a single product (by ID). If omitted, run for all products.",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear old suggestions before regenerating.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        product_id = options.get("product_id")
        clear = options.get("clear")

        qs = Product.objects.all()
        if product_id:
            qs = qs.filter(id=product_id)
            if not qs.exists():
                raise CommandError(f"Product id={product_id} not found.")

        total = qs.count()
        self.stdout.write(self.style.NOTICE(f"Found {total} product(s)."))

        done = 0
        for p in qs.iterator():
            if clear:
                PriceSuggestion.objects.filter(product=p).delete()
                LogisticsInfo.objects.filter(product=p).delete()

            generate_pricing_and_logistics(p)
            done += 1
            self.stdout.write(f"✓ Regenerated for product #{p.id}: {p.name}")

        self.stdout.write(self.style.SUCCESS(f"Done. Regenerated: {done} product(s)."))
