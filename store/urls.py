from django.urls import path
from django.urls import re_path

from .views import (category_list, featured_product, product_retrieve,category_retrieve,
                    products_list,search)

urlpatterns =[
    path('category',category_list,name='Category list'),
    # path('category/<int:id>',category_retrieve,name='Category list'),
    re_path(r'^category/(?P<slug>[\u0600-\u06FF-a-zA-Z0-9]+)$',category_retrieve,name="Category Retreive"),
    # re_path(r'^categories/(?P<slug>[\u0600-\u06FF-a-zA-Z0-9]+)$',category_retrieve,name="Cateogry Retreive"),
    path('featured-products',featured_product,name="Featured Product List"),
    path('products',products_list,name="Products List"),
    # path('products/<slug:slug>',product_retrieve, name="Product Retrieve")
    re_path(r'^products/(?P<slug>[\u0600-\u06FF-a-zA-Z0-9]+)$',product_retrieve,name="Product Retreive"),
    re_path(r'^search/(?P<q>[\u0600-\u06FF-a-zA-Z0-9]+)$',search,name="Products Search"),
]

    # re_path(r'^store/(?P<slug>[\u0600-\u06FF-a-zA-Z0-9]+)$', ProductRetrieveView.as_view(),name="store-product-retrieve"),
