from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Company(TimeStampedModel):
    name = models.CharField(max_length=255)
    street = models.CharField(max_length=255, blank=True)
    postal_code = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=128, blank=True)
    country = models.CharField(max_length=64, default="NL")
    vat_number = models.CharField(max_length=64, blank=True)
    iban = models.CharField(max_length=34, blank=True)
    currency = models.CharField(max_length=3, default="EUR")
    invoice_prefix = models.CharField(max_length=16, default="INV")
    invoice_next_number = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class Brand(TimeStampedModel):
    name = models.CharField(max_length=255)
    logo_url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="brands")

    class Meta:
        unique_together = ("name", "company")
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class SalesChannel(TimeStampedModel):
    class ChannelType(models.TextChoices):
        BOL = "BOL", "Bol.com"
        SHOPIFY = "SHOPIFY", "Shopify"
        OTHER = "OTHER", "Other"

    name = models.CharField(max_length=255)
    type = models.CharField(max_length=16, choices=ChannelType.choices)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="sales_channels")
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True, related_name="sales_channels")
    channeldock_id = models.CharField(max_length=128, blank=True)
    pricing_margin_target = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    pricing_notes = models.TextField(blank=True)

    class Meta:
        unique_together = ("name", "company")
        ordering = ("name",)

    def __str__(self) -> str:
        return f"{self.name} ({self.company.name})"
