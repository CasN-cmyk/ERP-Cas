from __future__ import annotations

from typing import Any, Dict

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from catalog.models import Product
from core.channeldock_client import ChannelDockClient, get_client
from core.models import Brand, Company, SalesChannel
from sales.models import Customer, Order, OrderLine


class Command(BaseCommand):
    help = "Synchronise products, inventory and orders from ChannelDock."

    def add_arguments(self, parser):
        parser.add_argument('--since', dest='since', help='ISO date string for incremental order sync', default=None)

    def handle(self, *args, **options):
        api_key = settings.CHANNELDOCK_API_KEY
        if not api_key:
            raise CommandError('CHANNELDOCK_API_KEY is not configured')

        client = get_client(api_key=api_key)
        since = options.get('since')
        self.stdout.write(self.style.MIGRATE_HEADING('Syncing ChannelDock data...'))

        try:
            self.sync_products(client)
            self.sync_orders(client, since)
        except NotImplementedError:
            raise CommandError('ChannelDock client methods are not implemented yet.')

        self.stdout.write(self.style.SUCCESS('ChannelDock sync completed'))

    def sync_products(self, client: ChannelDockClient):
        self.stdout.write('Syncing products...')
        for payload in client.fetch_products():
            ean = payload.get('ean')
            if not ean:
                continue
            brand = self._resolve_brand(payload)
            defaults = {
                'internal_id': payload.get('internal_id') or payload.get('sku') or ean,
                'sku': payload.get('sku', ''),
                'base_title': payload.get('title', f'Product {ean}'),
                'brand': brand,
                'category': payload.get('category', ''),
                'weight': payload.get('weight'),
                'width': payload.get('width'),
                'height': payload.get('height'),
                'length': payload.get('length'),
                'active': payload.get('active', True),
            }
            Product.objects.update_or_create(ean=ean, defaults=defaults)

    def sync_orders(self, client: ChannelDockClient, since: str | None = None):
        self.stdout.write('Syncing orders...')
        for payload in client.fetch_orders(since=since):
            sales_channel = self._resolve_sales_channel(payload)
            if not sales_channel:
                self.stderr.write(f"Skipping order {payload.get('id')} - sales channel missing")
                continue

            customer = self._upsert_customer(payload.get('customer', {}))
            order_defaults = self._build_order_defaults(payload, sales_channel, customer)
            order, _created = Order.objects.update_or_create(
                external_id=payload.get('id'), defaults=order_defaults
            )
            self._sync_order_lines(order, payload.get('lines', []))

    def _resolve_brand(self, payload: Dict[str, Any]) -> Brand:
        company = Company.objects.first()
        if not company:
            raise CommandError('At least one Company must exist to sync products.')
        brand_name = payload.get('brand') or 'Default Brand'
        brand, _ = Brand.objects.get_or_create(name=brand_name, company=company, defaults={'description': ''})
        return brand

    def _resolve_sales_channel(self, payload: Dict[str, Any]) -> SalesChannel | None:
        channel_id = payload.get('sales_channel_id') or payload.get('channel', {}).get('id')
        if not channel_id:
            return None
        return SalesChannel.objects.filter(channeldock_id=str(channel_id)).first()

    def _upsert_customer(self, data: Dict[str, Any]) -> Customer:
        email = data.get('email') or f"guest-{data.get('id', 'unknown')}@example.com"
        defaults = {
            'first_name': data.get('first_name', ''),
            'last_name': data.get('last_name', ''),
            'phone': data.get('phone', ''),
            'shipping_street': data.get('street', ''),
            'shipping_postal_code': data.get('postal_code', ''),
            'shipping_city': data.get('city', ''),
            'country': data.get('country', 'NL'),
        }
        customer, _ = Customer.objects.update_or_create(email=email, defaults=defaults)
        return customer

    def _build_order_defaults(
        self,
        payload: Dict[str, Any],
        sales_channel: SalesChannel,
        customer: Customer | None,
    ) -> Dict[str, Any]:
        company = sales_channel.company
        totals = payload.get('totals', {})
        source_system = payload.get('source_system', Order.SourceSystem.CHANNELDOCK)
        payment_status = payload.get('payment_status')
        if not payment_status and sales_channel.type in {SalesChannel.ChannelType.BOL, SalesChannel.ChannelType.SHOPIFY}:
            payment_status = Order.PaymentStatus.PAID
        elif not payment_status:
            payment_status = Order.PaymentStatus.UNPAID

        return {
            'external_channel_order_id': payload.get('channel_order_id', ''),
            'sales_channel': sales_channel,
            'company': company,
            'customer': customer,
            'order_date': payload.get('order_date'),
            'status': payload.get('status', Order.Status.NEW),
            'source_system': source_system,
            'payment_status': payment_status,
            'total_gross': totals.get('gross', 0),
            'total_net': totals.get('net', 0),
            'total_vat': totals.get('vat', 0),
            'currency': totals.get('currency', 'EUR'),
            'notes': payload.get('internal_notes', ''),
        }

    @transaction.atomic
    def _sync_order_lines(self, order: Order, lines: list[Dict[str, Any]]):
        order.lines.all().delete()
        for line in lines:
            product = None
            ean = line.get('ean')
            if ean:
                product = Product.objects.filter(ean=ean).first()
            OrderLine.objects.create(
                order=order,
                product=product,
                ean=ean or '',
                sku=line.get('sku', ''),
                title=line.get('title', ''),
                quantity=line.get('quantity', 1),
                unit_price=line.get('unit_price', 0),
                total_price=line.get('total_price', 0),
                vat_rate=line.get('vat_rate', 21),
            )
