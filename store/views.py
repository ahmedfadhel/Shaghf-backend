from django.db.models.aggregates import Count
from random import randint
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import OptionValue, Product, Tag,Category
from .serializers import OptionValueSerializer, ProductSerializer, TagSerializer,CategorySerializer


@api_view(['GET'])
def products_list(request):
    try:
        products = OptionValue.objects.filter(is_main=True)
        # products = OptionValue.objects.all()
        serializer = OptionValueSerializer(products,many=True,context={'request': request})
        
        return Response(serializer.data,status=status.HTTP_200_OK)
    except:
        return Response(serializer.error_messages,status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])
def featured_product(request):
    try:
        # featured_product = Product.objects.filter(is_featured = True)
        featured_product = OptionValue.objects.filter(product__is_featured=True,is_main=True)
        serializer = OptionValueSerializer(featured_product,many=True,context={'request': request})
        return Response(serializer.data,status = status.HTTP_200_OK)
    except:
        return Response('error',status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def product_retrieve(request,slug):
    try:
        product = Product.objects.get(slug=slug)
        if(product.product_options.all()[0].option.name == 'qu'):
            related_products = OptionValue.objects.filter(option__name = 'ge',is_main=True).exclude(prodcut__slug =slug)
        else:
            related_products = OptionValue.objects.filter(option__name = product.product_options.all()[0].option.name,is_main=True).exclude(product__slug = slug)
        if(related_products.count() == 1):
            related_products = OptionValue.objects.filter(option__name = product.product_options.all()[0].option.name,is_main=True).exclude(product__slug = slug)

            x = 1
        else:

            x = randint(0,related_products.count()-3)
        related_products_serializer = OptionValueSerializer(related_products[x:x+3],context={'request':request},many=True)    
        serializer = ProductSerializer(product,context={'request': request})
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
    serializer = OptionValueSerializer(products,context={"request":request},many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)
   
        

@api_view(['Get'])
def tags_list(request):
    if request.method == 'GET':
        tags = Tag.objects.all()
        serializer = TagSerializer(tags,many=True)
        return Response(serializer.data,status.HTTP_200_OK)
