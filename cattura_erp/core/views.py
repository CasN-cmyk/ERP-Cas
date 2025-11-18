from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render
from django.utils import timezone

from catalog.models import Product
from sales.models import Order


@login_required
def dashboard(request):
    now = timezone.now()
    last_7 = now - timedelta(days=7)
    last_30 = now - timedelta(days=30)

    orders_last_7 = Order.objects.filter(order_date__gte=last_7)
    orders_last_30 = Order.objects.filter(order_date__gte=last_30)

    context = {
        "orders_last_7": orders_last_7.count(),
        "orders_last_30": orders_last_30.count(),
        "revenue_last_30": orders_last_30.aggregate(total=Sum("total_gross"))["total"] or 0,
        "low_stock_products": Product.objects.filter(min_stock__gt=0).order_by("min_stock")[:10],
    }
    return render(request, "core/dashboard.html", context)
