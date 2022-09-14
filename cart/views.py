from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist

from cart.models import (Order)
from store.models import OptionValue
from .serializers import(
    OrderSerializer,
    ShippingInfoSerializer,
    OrderItemSerializer
)
# Create your views here.
@api_view(['GET'])
def list_orders(request):
    orders = Order.objects.all()
    order_serializer = OrderSerializer(orders,many=True)
    return Response(order_serializer.data,status=status.HTTP_200_OK)

@api_view(['POST'])
def order_status(request):
    order_ref = request.data.pop('order_ref',None)
    order_new_status = request.data.pop('order_status',None)
    if(order_new_status and order_ref):
        try:
            order = Order.objects.get(ref_code = order_ref)
            order.order_status = order_new_status
            order.save()
            
        except ObjectDoesNotExist:
            return Response({
                'message':'الطلب ذو العدد '+str(order_ref) + ' غير موجود',
                'status':404
                },status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({
            'message':'المعلومات غير صحيحة',
            'status':400
        },status=status.HTTP_400_BAD_REQUEST)
    order_serializer = OrderSerializer(order)
    return Response(order_serializer.data,status=status.HTTP_200_OK)


@api_view(['GET'])
def retreive_order(request,code):
    try:
        order = Order.objects.prefetch_related('items').get(ref_code = code)
        order_serializer = OrderSerializer(order,context={'request':request})
        return Response(order_serializer.data,status=status.HTTP_200_OK)
        
    except:
        return Response('المعلومات غير صحيحة',status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def checkout(request):
    products = []
    shipping_serializer = ShippingInfoSerializer(data=request.data['shipping'],context={"request": request})
    if(shipping_serializer.is_valid()):
        shipping_info = shipping_serializer.save()        
        order = Order.objects.create(shipping=shipping_info)
        for item in request.data['cart']:
            product = OptionValue.objects.filter(id = item['product']).first()
            if(product is not None):
                qty = item.pop('qty',None)
                if(product.is_discount):
                    price = product.discount_price                    
                else:
                    price = product.price
                if(product.in_stock >= qty):
                    order_item_serializer = OrderItemSerializer(data={
                    'product':product.id,
                    'qty':qty,
                    'price':price},context={"request": request})
                    if(order_item_serializer.is_valid()):
                        order_item = order_item_serializer.save()
                        products.append(order_item)
                    else:
                        if(len(products)):
                            for product in products:
                                product.delete()
                        order.delete()
                        return Response(order_item_serializer.errors)
                    if(product.option.name == 'qu'):
                        print('here')
                        for op in product.product.product_options.all():
                            op.in_stock = op.in_stock - qty
                            op.save()
                    product.in_stock = product.in_stock - qty
                    product.save()
                else:
                    if(len(products)):
                        for product in products:
                            product.delete()
                    order.delete()
                    return Response({
                        'message':'لم يتم تثبيت الطلب'
                    },status=status.HTTP_400_BAD_REQUEST)
            else:
                if(len(products)):
                    for product in products:
                        product.delete()
                order.delete()
                return Response('البيانات غير صحيحة',status=status.HTTP_400_BAD_REQUEST)
        order.items.set(products)
    else:
        return Response("معلومات الشحن غير صحيحة",status=status.HTTP_400_BAD_REQUEST)
    order_serializer = OrderSerializer(order)
    
    return Response({
        
       'message': 'تم تثبيت الطلب بنجاح',
       'status':201
        },status=status.HTTP_201_CREATED)


@api_view(['POST'])
def follow_order(request):
    phone = request.data.get('phone',None)
    if(phone):
        orders = Order.objects.filter(shipping__phone = phone).order_by('-updated_at')
        serializer = OrderSerializer(orders,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    else:
        return Response('يرجى ملئ رقم الهاتف',status=status.HTTP_400_BAD_REQUEST)