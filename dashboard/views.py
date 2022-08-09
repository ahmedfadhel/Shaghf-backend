

from django.db import IntegrityError
from rest_framework import status
from rest_framework.decorators import api_view,parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from store.models import Category, Option, OptionValue, Product, Tag

from .serializers import (CategorySerializer, OptionSerializer, OptionValueSerializer, ProductManageSerializer,
                          ProductSerializer, TagSerializer)


# list Tags function
@api_view(['Get'])
def tags_list(request):
    if request.method == 'GET':
        tags = Tag.objects.all()
        serializer = TagSerializer(tags,many=True)
        return Response(serializer.data,status.HTTP_200_OK)

# create Tags function
@api_view(['POST'])
def tag_create(request):
    serializer = TagSerializer(data= request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status = status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# update Tags function
@api_view(['GET','PATCH'])
def tag_update(request,id):
    if request.method == 'GET':
        try:
            tag = Tag.objects.get(id=id)
            serializer = TagSerializer(tag)
            return Response(serializer.data,status=status.HTTP_200_OK)

        except Tag.DoesNotExist:
            return Response({
                'message':'العنصر غير موجود',
                'status':400
            },status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        
        try:
            tag = Tag.objects.get(id=id)
            serializer = TagSerializer(tag,data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()            
            return Response(serializer.data,status=status.HTTP_200_OK)
            
        except(Tag.DoesNotExist,IntegrityError):
            
            return Response({
                'message':'العنصر غير موجود',
                'status':404
            },status=status.HTTP_404_NOT_FOUND)


# delete Tags function
@api_view(['DELETE'])
def tag_delete(request,id):
    try:
        tag = Tag.objects.get(id=id)
        tag.delete()
        return Response('Element deleted successfully',status=status.HTTP_204_NO_CONTENT)

    except(Tag.DoesNotExist):
        return Response({
            'message':'العنصر غير موجود',
            'status':404
        },status=status.HTTP_404_NOT_FOUND)


# list Category function
@api_view(['GET'])
def category_list(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories,many=True, context={'request': request})
    return Response(serializer.data,status=status.HTTP_200_OK)

# create Category function
@api_view(['POST'])
def category_create(request):

    serialiazer = CategorySerializer(data=request.data,context={'request': request})
    if serialiazer.is_valid(raise_exception=True):
        serialiazer.save()
        return Response(serialiazer.data,status=status.HTTP_201_CREATED)
    else:
        return Response(serialiazer.errors,status=status.HTTP_400_BAD_REQUEST)

# update Category function
@api_view(['GET','PATCH'])
def category_update(request,id):
    if request.method == 'GET':
        try:
            category = Category.objects.get(id=id)
            serializer = Category(category)
            return Response(serializer.data,status=status.HTTP_200_OK)

        except Category.DoesNotExist:
            return Response("Not found",status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'PATCH':
        try:
            category = Category.objects.get(id=id)
            serializer = CategorySerializer(category,data=request.data,partial=True,context={'request': request})
            print(request.data)
            if serializer.is_valid(raise_exception=True):
                # delete old image from the storage
                if(request.data.get('thumbnail')):
                    category.thumbnail.delete()
                    # print(request.data)
                # save the instance with new values
                serializer.save()            
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            
        except(Category.DoesNotExist,IntegrityError):
            return Response({
                'message':'العنصر غير موجود',
                'status':404
            },status=status.HTTP_404_NOT_FOUND)


# delete Categroy Function
@api_view(['DELETE'])
def categroy_delete(request,id):
    try:
        category = Category.objects.get(id=id)
        category.thumbnail.delete()
        category.delete()
        return Response('Elemented deleted Successfully',status=status.HTTP_204_NO_CONTENT)
    except Category.DoesNotExist:
        return Response({
            'message':'العنصر غير موجود',
            'status':404
        },status=status.HTTP_404_NOT_FOUND)

# list Products function
@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products,many=True,context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def product_retrieve(request,id):
    try:
        product = Product.objects.get(id=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data,status=status.HTTP_200_OK)
    except Product.DoesNotExist:
        return Response('Not Found',status=status.HTTP_400_BAD_REQUEST)
# create Product function
@api_view(['POST'])
def product_create(request):

    serializer = ProductManageSerializer(data=request.data)
    try:
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data,status=status.HTTP_200_OK)
    except :
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['PATCH'])
def product_edit(request,id):
    try:
        instance = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response({
            'message':'العنصر غير موجود',
           
        }, status = status.HTTP_404_NOT_FOUND)
    serializer = ProductManageSerializer(instance = instance,data=request.data,partial=True)
    if serializer.is_valid():
        serializer.save()
    else:
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.data,status=status.HTTP_200_OK)
# delete Product Function
@api_view(['DELETE'])
def product_delete(request,id):
    
    try:
        product= Product.objects.get(id=id)
        product.delete()
        return Response('Elemented deleted Successfully',status=status.HTTP_204_NO_CONTENT)
    except Product.DoesNotExist:
        return Response({
            'message':'العنصر غير موجود',
            'status':404
        },status=status.HTTP_404_NOT_FOUND)

# list options
@api_view(['GET'])
def option_list(request):
    try:
        options = Option.objects.all()
        serializer = OptionSerializer(options,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    except:
        return Response('Not Found',status=status.HTTP_400_BAD_REQUEST)


# list Product options
@api_view(['GET'])
def options_value_list(request,id):
    try:
        
        product_options = OptionValue.objects.filter(product=id)
        option_values_serializer = OptionValueSerializer(product_options,many=True,context={'request': request} )
        return Response(option_values_serializer.data,status=status.HTTP_200_OK)
    except OptionValue.DoesNotExist:
        return Response('Not Fount',status=status.HTTP_204_NO_CONTENT)

# Create Option function
@api_view(['POST'])
@parser_classes([MultiPartParser])
def option_value_create(request):
   
    try:
        serializer = OptionValueSerializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
        return Response({
            'id':serializer.data['id'],
            'name':serializer.data['name'],
            'option':serializer.data['option'],
            'price':serializer.data['price'],
            'product':serializer.data['product'],
            'is_main':serializer.data['is_main'],

            },status=status.HTTP_200_OK)
    except:
    
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# update Option function
@api_view(['PATCH'])
def option_value_edit(request,id):
    try:
        instance = OptionValue.objects.get(id=id)
    except OptionValue.DoesNotExist:
        return Response({
            'message':'العنصر غير موجود'    
        },status=status.HTTP_404_NOT_FOUND)   

    serializer = OptionValueSerializer(instance = instance,data=request.data,partial=True)
    if serializer.is_valid():
        serializer.save()
    else:
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Delete Option function
@api_view(['DELETE'])
def option_value_delete(request,id):
    try:
      
        option_value = OptionValue.objects.get(id=id)
        option_value.delete()
        return Response('',status=status.HTTP_204_NO_CONTENT)
    except OptionValue.DoesNotExist:
        return Response({
            'message':"العنصر غير موجود"
        },status=status.HTTP_404_NOT_FOUND)