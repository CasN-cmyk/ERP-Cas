from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import ListView

from core.models import SalesChannel
from .models import Order


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'sales/order_list.html'
    context_object_name = 'orders'
    paginate_by = 25

    def get_queryset(self):
        queryset = super().get_queryset().select_related('customer', 'sales_channel')
        search = self.request.GET.get('search')
        channel = self.request.GET.get('sales_channel')
        payment_status = self.request.GET.get('payment_status')
        source_system = self.request.GET.get('source_system')
        if search:
            queryset = queryset.filter(
                Q(external_id__icontains=search)
                | Q(external_channel_order_id__icontains=search)
                | Q(customer__email__icontains=search)
            )
        if channel:
            queryset = queryset.filter(sales_channel_id=channel)
        if payment_status:
            queryset = queryset.filter(payment_status=payment_status)
        if source_system:
            queryset = queryset.filter(source_system=source_system)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sales_channels'] = SalesChannel.objects.all()
        context['payment_choices'] = Order.PaymentStatus.choices
        context['source_choices'] = Order.SourceSystem.choices
        query_dict = self.request.GET.copy()
        query_dict.pop('page', None)
        context['querystring'] = query_dict.urlencode()
        return context
