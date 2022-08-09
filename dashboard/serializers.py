
from rest_framework import serializers

from store.models import Category, Image, Option, OptionValue, Product, Tag


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model   = Tag
        fields  = ['id','name','slug','updated_at']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['id','name','description','slug','thumbnail','updated_at']

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields='__all__'
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id','name','description','category','tags','is_featured','updated_at']
        depth=1

class ProductManageSerializer(serializers.ModelSerializer):
    tags_id = serializers.PrimaryKeyRelatedField(queryset = Tag.objects.all(),many=True,write_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset = Category.objects.all(),write_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(read_only=True,many=True)
    class Meta:
        model=Product
        fields=['id','name','description','tags','category','is_featured','updated_at','tags_id','category_id']
        depth=1

    def create(self,validated_data):
        category = validated_data.pop('category_id')
        tags = validated_data.pop('tags_id')
        product = Product.objects.create(**validated_data,category=category)
        product.save()
        product.tags.set(tags)
        return product
    def update(self,instance,validated_data):
        category = validated_data.pop('category_id',None)
        tags = validated_data.pop('tags_id',None)
        instance.name = validated_data.get('name',instance.name)
        instance.description = validated_data.get('description',instance.description)
        instance.is_featured = validated_data.get('is_featured',instance.is_featured)
        instance.save()
        if(category):
            instance.category = category

        if(tags):
            instance.tags.set(tags)
        instance.save()
        print(instance.tags.all())
        return instance
class OptionSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    class Meta:
        model=Option
        fields = "__all__"

    def get_name(self,obj):
        return obj.get_name_display()

class OptionValueSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(queryset = Product.objects.all(),write_only=True)
    option_id = serializers.PrimaryKeyRelatedField(queryset = Option.objects.all(),write_only=True)


    thumbnail_path = serializers.ImageField(write_only=True)
    thumbnail_alt_text = serializers.CharField(write_only=True)

    product = ProductSerializer(read_only=True)
    option=OptionSerializer(read_only=True)
    thumbnail = ImageSerializer(read_only=True)
    class Meta:
        model = OptionValue
        fields='__all__'
        depth=1

    def create(self,validated_data):
        path = validated_data.pop('thumbnail_path')
        alt_text = validated_data.pop('thumbnail_alt_text')

        image = Image.objects.create(path=path,alt_text=alt_text)
        image.save()
        product= validated_data.pop('product_id')
        option = validated_data.pop('option_id')
        option_value = OptionValue.objects.create(**validated_data,option=option,product=product,thumbnail=image)
        option_value.save()
        return option_value

    def update(self,instance,validated_data):
        instance.name = validated_data.get('name',instance.name)
        instance.value = validated_data.get('value',instance.value)
        instance.price = validated_data.get('price',instance.price)
        instance.purchase_price = validated_data.get('purchase_price',instance.purchase_price)
        instance.is_discount = validated_data.get('is_discount',instance.is_discount)
        instance.discount_price = validated_data.get('discount_price',instance.discount_price)
        instance.is_main = validated_data.get('is_main',instance.is_main)
        instance.sku = validated_data.get('sku',instance.sku)
        instance.in_stock = validated_data.get('in_stock',instance.in_stock)
        if(validated_data.get('option_id')):
          instance.option = validated_data.get('option_id') 
          instance.option.save()

        if(validated_data.get('thumbnail_path',None)):
            instance.thumbnail.path.delete() 
            instance.thumbnail.path = validated_data.get('thumbnail_path')
            instance.thumbnail.save()
        if(validated_data.get('thumbnail_alt_text')):
            instance.thumbnail.alt_text = validated_data.get('thumbnail_alt_text',instance.thumbnail.alt_text)
            instance.thumbnail.save()
        instance.save()
        return instance