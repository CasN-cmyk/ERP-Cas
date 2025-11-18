from django.contrib import admin

from .models import Customer, CustomerLabel, Order, OrderLine


@admin.register(CustomerLabel)
class CustomerLabelAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "created_at")
    search_fields = ("name",)


class OrderLineInline(admin.TabularInline):
    model = OrderLine
    extra = 0


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "last_name", "country")
    search_fields = ("email", "first_name", "last_name", "phone")
    list_filter = ("country", "labels")
    filter_horizontal = ("labels",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "external_id",
        "sales_channel",
        "customer",
        "order_date",
        "status",
        "payment_status",
        "total_gross",
    )
    search_fields = ("external_id", "external_channel_order_id", "customer__email")
    list_filter = ("sales_channel", "status", "payment_status", "source_system")
    inlines = [OrderLineInline]
