from django.urls import path

from .views import (category_create, category_list, category_update,
                    categroy_delete, option_list, option_value_create,
                    option_value_delete, option_value_edit, options_value_list,
                    product_create, product_delete, product_edit, product_list,
                    product_retrieve, tag_create, tag_delete, tag_update,
                    tags_list)

urlpatterns =[
    path('tags',tags_list,name='Tags list'),
    path('tags/create',tag_create,name="Tag Create"),
    path('tags/<int:id>/edit',tag_update,name="Tag Update"),
    path('tags/delete/<int:id>',tag_delete,name="Tag Delete"),
    path('category',category_list,name="Categories list"),
    path('category/create',category_create,name="Category Create"),
    path('category/<int:id>/edit',category_update,name="Category Update"),
    path('category/delete/<int:id>',categroy_delete,name="Category Delete"),
    path('options',option_list,name="Options List"),
    path('products',product_list,name="Product List"),
    path('product/create',product_create,name="Product Create"),
    path('product/<int:id>/edit',product_edit,name="Product Edit"),
    path('product/view/<int:id>',product_retrieve,name="Product Retrieve"),
    path('products/delete/<int:id>',product_delete,name="Product Delete"),
    path('product/<int:id>/option-values',options_value_list,name="Product Option Values list"),
    path('product/option-values/create',option_value_create,name="Product Option Values Create"),
    path('product/option-values/<int:id>/edit',option_value_edit,name="Product Option Values Edit"),
    path('product/option-values/delete/<int:id>',option_value_delete,name="Product Option Values Delete"),

]
