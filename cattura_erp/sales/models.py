from django.db import models

from catalog.models import Product
from core.models import Company, SalesChannel, TimeStampedModel


class CustomerLabel(TimeStampedModel):
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.name


class Customer(TimeStampedModel):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=128, blank=True)
    last_name = models.CharField(max_length=128, blank=True)
    phone = models.CharField(max_length=64, blank=True)
    shipping_street = models.CharField(max_length=255, blank=True)
    shipping_postal_code = models.CharField(max_length=32, blank=True)
    shipping_city = models.CharField(max_length=128, blank=True)
    country = models.CharField(max_length=64, default="NL")
    billing_same_as_shipping = models.BooleanField(default=True)
    billing_street = models.CharField(max_length=255, blank=True)
    billing_postal_code = models.CharField(max_length=32, blank=True)
    billing_city = models.CharField(max_length=128, blank=True)
    labels = models.ManyToManyField(CustomerLabel, blank=True, related_name="customers")

    class Meta:
        ordering = ("email",)

    def __str__(self) -> str:
        return self.email


class Order(TimeStampedModel):
    class Status(models.TextChoices):
        NEW = "NEW", "New"
        PROCESSING = "PROCESSING", "Processing"
        SHIPPED = "SHIPPED", "Shipped"
        CANCELLED = "CANCELLED", "Cancelled"
        RETURNED = "RETURNED", "Returned"
        COMPLETED = "COMPLETED", "Completed"

    class SourceSystem(models.TextChoices):
        CHANNELDOCK = "CHANNELDOCK", "ChannelDock"
        MANUAL = "MANUAL", "Manual"

    class PaymentStatus(models.TextChoices):
        PAID = "PAID", "Paid"
        UNPAID = "UNPAID", "Unpaid"
        PARTIALLY_PAID = "PARTIALLY_PAID", "Partially paid"

    external_id = models.CharField(max_length=128, unique=True)
    external_channel_order_id = models.CharField(max_length=128, blank=True)
    sales_channel = models.ForeignKey(SalesChannel, on_delete=models.PROTECT, related_name="orders")
    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name="orders")
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, related_name="orders")
    order_date = models.DateTimeField()
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.NEW)
    source_system = models.CharField(max_length=16, choices=SourceSystem.choices, default=SourceSystem.CHANNELDOCK)
    payment_status = models.CharField(max_length=16, choices=PaymentStatus.choices, default=PaymentStatus.PAID)
    total_gross = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_net = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_vat = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, default="EUR")
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ("-order_date",)

    def __str__(self) -> str:
        return f"Order {self.external_id}"


class OrderLine(TimeStampedModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="lines")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    ean = models.CharField(max_length=13, blank=True)
    sku = models.CharField(max_length=64, blank=True)
    title = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    vat_rate = models.DecimalField(max_digits=4, decimal_places=2, default=21)

    def __str__(self) -> str:
        return f"{self.title} x {self.quantity}"
