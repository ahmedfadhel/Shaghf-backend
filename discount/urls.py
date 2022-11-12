from django.urls import path
from .views import check_code,code_create,code_update_retreive,delete_code
urlpatterns =[
    path('check/<str:code>/',check_code,name='Check Discount Code'),
    path('create',code_create,name='Create New Discount Code'),
    path('<int:id>/update',code_update_retreive,name='Retreive And Update Discount Code'),
    path('<int:id>/delete',delete_code,name='Delete Discount Code')
]