from rest_framework import serializers
from .models import (
    Discount
)

class DiscountSerializer(serializers.ModelSerializer):
    is_active = serializers.ReadOnlyField()
    class Meta:
        model = Discount
        fields = ('id','code','discount','discount_type','is_active','valid_to','valid_from')
        # fields = "__all__"