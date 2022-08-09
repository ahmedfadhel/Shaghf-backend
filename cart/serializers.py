
from wsgiref import validate
from rest_framework import serializers
from .models import (
    ShippingInfo,
    OrderItem,
    Order
)


class ShippingInfoSerializer(serializers.ModelSerializer):
    # gover = serializers.CharField(source='get_gover_display',read_only=True)
    class Meta:
        model  = ShippingInfo
        fields = '__all__'
  
    def create(self,validated_data):
       
        shipping , created = ShippingInfo.objects.get_or_create(
            phone = validated_data['phone'],
            gover = validated_data['gover'],
            city = validated_data['city'],
            defaults={
                **validated_data
            }
        )

        return shipping
    def __init__(self, *args, **kwargs):
        super(ShippingInfoSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.method=='POST':
            self.fields['gover'] = serializers.CharField()
        else:
            self.fields['gover'] = serializers.CharField(source='get_gover_display',read_only=True)
            
class OrderItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = OrderItem
        fields="__all__"

    def __init__(self, *args, **kwargs):
        super(OrderItemSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.method=='POST':
            self.Meta.depth = 0
        else:
            self.Meta.depth = 2

class OrderSerializer(serializers.ModelSerializer):
    shipping = ShippingInfoSerializer()
    class Meta:
        model = Order
        fields ="__all__"
        depth=1

    def __init__(self, *args, **kwargs):
        super(OrderSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
       
        if request and request.method=='GET':
            self.fields['items'] = OrderItemSerializer(many=True)