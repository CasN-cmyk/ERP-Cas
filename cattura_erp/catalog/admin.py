from django.contrib import admin

from .models import Product, ProductChannel, ProductLabel


@admin.register(ProductLabel)
class ProductLabelAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "created_at")
    search_fields = ("name",)


class ProductChannelInline(admin.TabularInline):
    model = ProductChannel
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("base_title", "ean", "sku", "brand", "lifecycle_status", "active", "min_stock")
    list_filter = ("brand", "lifecycle_status", "active", "labels")
    search_fields = ("base_title", "ean", "sku")
    inlines = [ProductChannelInline]
    filter_horizontal = ("labels",)


@admin.register(ProductChannel)
class ProductChannelAdmin(admin.ModelAdmin):
    list_display = ("product", "sales_channel", "is_active_on_channel", "channel_price", "desired_margin_percent")
    list_filter = ("sales_channel", "is_active_on_channel")
    search_fields = ("product__base_title", "sales_channel__name")
