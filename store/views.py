from random import sample
from django.db.models import Q

from django.db.models.aggregates import Count
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import Category, OptionValue, Product, Tag
from .serializers import (CategorySerializer, OptionValueSerializer,
                          ProductSerializer, TagSerializer)

class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'page':self.page.number,
            'page_size':self.page_size,
            'count': self.page.paginator.count,
            'results': data
        })
@api_view(['GET'])
def products_list(request):
    products = OptionValue.objects.filter(is_main=True)
    paginator = CustomPagination()
    paginator.page_size = 8
    result_page = paginator.paginate_queryset(products,request)
    serializer = OptionValueSerializer(result_page,many=True,context={'request': request})
    return  paginator.get_paginated_response(serializer.data)
@api_view(['GET'])
def featured_product(request):
    try:
        featured_product = OptionValue.objects.filter(product__is_featured=True,is_main=True)
        serializer = OptionValueSerializer(featured_product,many=True,context={'request': request})
        return Response(serializer.data,status = status.HTTP_200_OK)
    except:
        return Response('error',status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def product_retrieve(request,slug):
    try:
        product = Product.objects.get(slug=slug)
        serializer = ProductSerializer(product,context={'request': request})
        if(product.product_options.all()[0].option.name == 'qu'):
           
            related_products = OptionValue.objects.filter(option__name = 'ge',is_main=True)
        else:
            related_products = OptionValue.objects.filter(option__name = product.product_options.all()[0].option.name,is_main=True).exclude(product__slug = slug)
        
        related_products = list(related_products)
        if(len(related_products) >= 4):
            related_products = sample(related_products,4)
        
        related_products_serializer = OptionValueSerializer(related_products,context={'request':request},many=True)    
        return Response({
            'product':serializer.data,
            'related_products':related_products_serializer.data

        },status=status.HTTP_200_OK)
    except:
        return Response(serializer.error_messages,status=status.HTTP_400_BAD_REQUEST)

@api_view(['Get'])
def category_list(request):
    try:
        categories = Category.objects.all()
        serializer = CategorySerializer(categories,many=True,context={'request': request})
        return Response(serializer.data,status=status.HTTP_200_OK)
    except:
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def category_retrieve(request,slug):
    products = OptionValue.objects.filter(product__category__slug = slug , is_main=True)
    if(len(products) < 1):
        return Response('Not Found',status=status.HTTP_404_NOT_FOUND)
    paginator = CustomPagination()
    paginator.page_size = 12
    result_page = paginator.paginate_queryset(products,request)
    serializer = OptionValueSerializer(result_page,context={"request":request},many=True)
    # return Response(serializer.data,status=status.HTTP_200_OK)
    return  paginator.get_paginated_response(serializer.data)

   
        

@api_view(['Get'])
def tags_list(request):
    if request.method == 'GET':
        tags = Tag.objects.all()
        serializer = TagSerializer(tags,many=True)
        return Response(serializer.data,status.HTTP_200_OK)

@api_view(['GET'])
def search(request,q):
    print(q)
    search_products = OptionValue.objects.filter( Q(name__icontains = q) | Q(product__name__icontains=q))
    search_products = search_products.filter(is_main=True)
    print(search_products)
    serializer = OptionValueSerializer(search_products,many=True,context={"request":request})
    return Response(serializer.data,status=status.HTTP_200_OK)