from django.urls import path
from .views import check_code,code_create,code_update_retreive,delete_code,code_list
urlpatterns =[
    path('coupons',code_list,name='Check Discount Code'),
    path('coupon/check/<str:code>/',check_code,name='Check Discount Code'),
    path('coupon/create',code_create,name='Create New Discount Code'),
    path('coupon/<int:id>/update',code_update_retreive,name='Retreive And Update Discount Code'),
    path('coupon/<int:id>/delete',delete_code,name='Delete Discount Code')
]