from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import ListView

from core.models import Brand
from .models import Product


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'
    paginate_by = 25

    def get_queryset(self):
        queryset = super().get_queryset().select_related('brand')
        search = self.request.GET.get('search')
        lifecycle = self.request.GET.get('lifecycle_status')
        brand = self.request.GET.get('brand')
        if search:
            queryset = queryset.filter(
                Q(base_title__icontains=search)
                | Q(ean__icontains=search)
                | Q(sku__icontains=search)
            )
        if lifecycle:
            queryset = queryset.filter(lifecycle_status=lifecycle)
        if brand:
            queryset = queryset.filter(brand_id=brand)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brands'] = Brand.objects.all()
        context['lifecycle_choices'] = Product.LifecycleStatus.choices
        query_dict = self.request.GET.copy()
        query_dict.pop('page', None)
        context['querystring'] = query_dict.urlencode()
        return context
