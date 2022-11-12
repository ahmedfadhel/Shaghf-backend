from rest_framework.decorators import api_view
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework import status
from datetime import date
from .models import (Discount)
from .serializers import (DiscountSerializer)
# Create your views here.

#Check Discount Code
@api_view(['GET'])
def check_code(self,code):
    # valid_code = Discount.objects.filter(code=code , valid_to__gt=date.today())
    valid_code = Discount.objects.filter(code=code)
    serializer = DiscountSerializer(valid_code,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)

# Create Discount Code
@api_view(['POST'])
def code_create(request):
    serializer = DiscountSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# Retrieve And Update Discount Code
@api_view(['GET','PUT'])
def code_update_retreive(request,id):
    if request.method == 'GET':
        try:
            discount = Discount.objects.get(id=id)
            serializer = DiscountSerializer(discount)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Discount.DoesNotExist:
            return Response({
                'message':'العنصر غير موجود',
                'status':400
            },status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PUT':
        try:

            discount = Discount.objects.get(id=id)
            serializer = DiscountSerializer(discount,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except (Discount.DoesNotExist,IntegrityError):
            return Response({
                'message':'العنصر غير موجود',
                'status':404
            },status=status.HTTP_404_NOT_FOUND)


# Delete Discount Code
@api_view(['Delete'])
def delete_code(request,id):
    try:
        discount = Discount.objects.get(id=id)
        discount.delete()
        return Response({
            'message':'تم حذف العنصر',
            'status':'204'
        },status=status.HTTP_204_NO_CONTENT)
    except Discount.DoesNotExist:
        return Response({
                'message':'العنصر غير موجود',
                'status':404
            },status=status.HTTP_404_NOT_FOUND)