from django.db import models

from core.models import Brand, SalesChannel, TimeStampedModel


class ProductLabel(TimeStampedModel):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class Product(TimeStampedModel):
    class LifecycleStatus(models.TextChoices):
        CONCEPT = "CONCEPT", "Concept"
        ACTIVE = "ACTIVE", "Active"
        REVIEW = "REVIEW", "Review"
        EOL = "EOL", "End of life"
        DISCONTINUED = "DISCONTINUED", "Discontinued"

    internal_id = models.CharField(max_length=64, unique=True)
    ean = models.CharField(max_length=13, unique=True)
    sku = models.CharField(max_length=64, blank=True)
    base_title = models.CharField(max_length=255)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name="products")
    category = models.CharField(max_length=128, blank=True)
    weight = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    width = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    height = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    length = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    active = models.BooleanField(default=True)
    lifecycle_status = models.CharField(max_length=16, choices=LifecycleStatus.choices, default=LifecycleStatus.CONCEPT)
    eol_date = models.DateField(null=True, blank=True)
    short_description = models.CharField(max_length=512, blank=True)
    long_description = models.TextField(blank=True)
    seo_title = models.CharField(max_length=255, blank=True)
    seo_description = models.CharField(max_length=512, blank=True)
    qa_score = models.PositiveSmallIntegerField(null=True, blank=True)
    qa_notes = models.TextField(blank=True)
    hs_code = models.CharField(max_length=32, blank=True)
    country_of_origin = models.CharField(max_length=64, blank=True)
    min_stock = models.PositiveIntegerField(default=0)
    target_stock_days = models.PositiveIntegerField(default=30)
    base_purchase_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    extra_cost_transport_per_unit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    extra_cost_customs_per_unit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    extra_cost_fulfilment_per_unit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    labels = models.ManyToManyField(ProductLabel, related_name="products", blank=True)

    class Meta:
        ordering = ("base_title",)

    def __str__(self) -> str:
        return f"{self.base_title} ({self.ean})"

    @property
    def landed_cost(self) -> float:
        return float(
            self.base_purchase_price
            + self.extra_cost_transport_per_unit
            + self.extra_cost_customs_per_unit
            + self.extra_cost_fulfilment_per_unit
        )


class ProductChannel(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="channel_settings")
    sales_channel = models.ForeignKey(SalesChannel, on_delete=models.CASCADE, related_name="product_settings")
    is_active_on_channel = models.BooleanField(default=False)
    channel_title_override = models.CharField(max_length=255, blank=True)
    channel_description_override = models.TextField(blank=True)
    channel_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    desired_margin_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    min_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    max_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        unique_together = ("product", "sales_channel")
        verbose_name = "Product channel configuration"
        verbose_name_plural = "Product channel configurations"

    def __str__(self) -> str:
        return f"{self.product} @ {self.sales_channel}"
