from django.urls import path

from .views import OrderListView

app_name = 'sales'

urlpatterns = [
    path('', OrderListView.as_view(), name='order-list'),
]
