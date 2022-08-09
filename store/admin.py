from msilib.schema import Media
from django.contrib import admin
from .models import Tag,Category,Product,Image,Option,OptionValue
# Register your models here.
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Image)
admin.site.register(Option)
admin.site.register(OptionValue)