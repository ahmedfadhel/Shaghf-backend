from django.urls import path
from .views import (checkout, list_orders, order_status, retreive_order)
urlpatterns =[
     path('orders',list_orders,name="List orders"),
     path('orders/retreive-order/<int:code>',retreive_order,name="Retreive order "),
     path('orders/update-order',order_status,name="Change order status"),
     path('checkout',checkout,name='Checkout'),
]