from django.urls import path
from cart.views import (follow_order)
urlpatterns =[
    path('track-order',follow_order,name='Track order status')
]