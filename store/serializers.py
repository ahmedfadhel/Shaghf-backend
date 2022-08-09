from rest_framework import serializers

from dashboard.serializers import ImageSerializer

from .models import Category, OptionValue, Product, Tag

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model= Category
        fields=['id','slug','name','description','thumbnail','product_category']
        depth=1

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model   = Tag
        fields  = ['id','name','slug','updated_at']


class OptionValueSerializer(serializers.ModelSerializer):

    class Meta:
        model = OptionValue
        fields = '__all__'
        depth = 2
        
class ProductSerializer(serializers.ModelSerializer):
    product_options = OptionValueSerializer(many=True)
 
    class Meta:
        model = Product
        fields = "__all__"
        depth = 1