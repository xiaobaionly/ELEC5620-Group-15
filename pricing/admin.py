# from django.contrib import admin
# from django.http import HttpResponse
# import csv
# from .models import PriceSuggestion, LogisticsInfo
#
#
# @admin.register(LogisticsInfo)
# class LogisticsInfoAdmin(admin.ModelAdmin):
#     """
#     Admin for LogisticsInfo.
#     Adds 'owner' column via product -> supplier -> user.
#     """
#     list_display = ("product", "region", "carrier", "cost_estimate", "estimated_days", "owner")
#     list_filter = (
#         "region",
#         "carrier",
#         ("product__supplier__user", admin.RelatedOnlyFieldListFilter),  # filter by owner
#     )
#     search_fields = (
#         "region",
#         "carrier",
#         "product__name",
#         "product__supplier__company_name",
#         "product__supplier__user__username",
#         "product__supplier__user__email",
#     )
#     autocomplete_fields = ("product",)
#     list_select_related = ("product", "product__supplier", "product__supplier__user")
#     list_per_page = 25
#     fieldsets = (
#         ("Target", {"fields": ("product", "region", "carrier")}),
#         ("Cost & ETA", {"fields": ("cost_estimate", "estimated_days")}),
#     )
#     actions = ["export_as_csv"]
#
#     def export_as_csv(self, request, queryset):
#         """Export selected records as CSV."""
#         response = HttpResponse(content_type="text/csv")
#         response["Content-Disposition"] = "attachment; filename=logisticsinfo.csv"
#         import csv
#         writer = csv.writer(response)
#         writer.writerow(["product", "region", "carrier", "cost_estimate", "estimated_days", "owner"])
#         for obj in queryset:
#             writer.writerow([obj.product, obj.region, obj.carrier, obj.cost_estimate, obj.estimated_days, self.owner(obj)])
#         return response
#     export_as_csv.short_description = "Export selected as CSV"
#
#     def owner(self, obj):
#         """Return user through product -> supplier -> user."""
#         supplier = getattr(obj.product, "supplier", None)
#         return getattr(supplier, "user", None)
#     owner.short_description = "User"
#     owner.admin_order_field = "product__supplier__user"
#
#
# @admin.register(PriceSuggestion)
# class PriceSuggestionAdmin(admin.ModelAdmin):
#     """
#     Admin for PriceSuggestion.
#     Adds 'owner' column via product -> supplier -> user.
#     """
#     list_display = ("product", "suggested_price", "created_at", "short_rationale", "owner")
#     list_filter = (
#         "created_at",
#         ("product__supplier__user", admin.RelatedOnlyFieldListFilter),  # filter by owner
#     )
#     search_fields = (
#         "product__name",
#         "rationale",
#         "product__supplier__company_name",
#         "product__supplier__user__username",
#         "product__supplier__user__email",
#     )
#     date_hierarchy = "created_at"
#     autocomplete_fields = ("product",)
#     list_select_related = ("product", "product__supplier", "product__supplier__user")
#     readonly_fields = ("created_at",)
#     list_per_page = 25
#     fieldsets = (
#         ("Result", {"fields": ("product", "suggested_price")}),
#         ("Rationale", {"fields": ("rationale",)}),
#         ("System", {"fields": ("created_at",), "classes": ("collapse",)}),
#     )
#
#     def short_rationale(self, obj):
#         """Truncate rationale for list display."""
#         return (obj.rationale[:40] + "…") if obj.rationale and len(obj.rationale) > 40 else obj.rationale
#     short_rationale.short_description = "Rationale"
#
#     def owner(self, obj):
#         """Return user through product -> supplier -> user."""
#         supplier = getattr(obj.product, "supplier", None)
#         return getattr(supplier, "user", None)
#     owner.short_description = "User"
#     owner.admin_order_field = "product__supplier__user"
