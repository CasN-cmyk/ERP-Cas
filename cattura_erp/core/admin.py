from django.contrib import admin

from .models import Brand, Company, SalesChannel


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "vat_number", "currency", "invoice_prefix", "invoice_next_number")
    search_fields = ("name", "vat_number", "iban")
    list_filter = ("country", "currency")


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "company", "logo_url")
    list_filter = ("company",)
    search_fields = ("name", "description")


@admin.register(SalesChannel)
class SalesChannelAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "company", "brand", "pricing_margin_target")
    list_filter = ("type", "company")
    search_fields = ("name", "channeldock_id")
