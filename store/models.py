from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.translation import gettext as _

from utils.models import TimestampMixin

from .utils import unique_slug_generator

# Create your models here.

# Category model

class Category(TimestampMixin,models.Model):
    name = models.CharField(_("Category Name"), max_length=50)
    slug = models.SlugField(_("Category User Friendly Name"),blank=True)
    description = models.TextField(_("Category Description"))
    thumbnail = models.ImageField(_("Category Thumbanil"), upload_to='categories')

    class Meta:
        ordering = ['-updated_at']
    def __str__(self):
        return self.name
@receiver(pre_save,sender=Category)
def category_pre_save(sender,instance,*args, **kwargs):
    if not instance.slug:
        instance.slug= unique_slug_generator(instance)
    else:
        old_instance = Category.objects.get(id=instance.id)
        if old_instance.name != instance.name:
            instance.slug = unique_slug_generator(instance)

class Tag(TimestampMixin,models.Model):
    name=models.CharField(_("Tag Name"), max_length=50)
    slug = models.SlugField(_("Tag User Friendly Name"),blank=True)
    def __str__(self) :
        return self.name

@receiver(pre_save,sender=Tag)
def tag_pre_save(sender,instance,*args, **kwargs):
    if not instance.slug:
        instance.slug= unique_slug_generator(instance)
    else:
        old_instance = Tag.objects.get(id=instance.id)
        if old_instance.name != instance.name:
            instance.slug = unique_slug_generator(instance)


class Product(TimestampMixin,models.Model):
    name            = models.CharField(_("Product Name"), max_length=75)
    slug            = models.SlugField(_("Product Friendly Name"),blank=True)
    description     = models.TextField(_("Product Description"))
    tags            = models.ManyToManyField(Tag, verbose_name=_("Product Tags"),related_name='product_tags')
    category        = models.ForeignKey(Category, verbose_name=_("Product Category"), on_delete=models.CASCADE,related_name='product_category')
    is_featured     = models.BooleanField(_("Is Product Featured?"),default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering=['-updated_at']
@receiver(pre_save,sender=Product)
def product_pre_save(sender,instance,*args, **kwargs):
    if not instance.slug:
        instance.slug= unique_slug_generator(instance)
    else:
        old_instance = Product.objects.get(id=instance.id)
        if old_instance.name != instance.name:
            instance.slug = unique_slug_generator(instance)
            
class Image(TimestampMixin, models.Model):
    path = models.ImageField(_("Image"), upload_to='products')
    alt_text = models.CharField(_("Media Alt Text"), max_length=100)

    def __str__(self):
        return self.alt_text

class Option(TimestampMixin,models.Model):
    option_choices =(
        ('ge','general'),
        ('co','colors'),
        ('qu','quantity')
    )

    name    = models.CharField(_("Option Name"), max_length=3,choices=option_choices)

    def __str__(self):
        return self.name


class OptionValue(TimestampMixin, models.Model):
    name            = models.CharField(_("Option Value Name"), max_length=50)
    value           = models.CharField(_('Option Value for Colors'),default="Code",max_length=50)
    price           = models.IntegerField(_("Option Value Price"))
    purchase_price  = models.IntegerField(_("Option Value Purchase Price"))
    is_discount     = models.BooleanField(_("Is Discount?"),default=False)
    discount_price  = models.IntegerField(_("Option Value Discount Price"))
    sku             = models.CharField(_("Option Value SKU Code"), max_length=10)
    in_stock        = models.IntegerField(_("Option Value In Stock"))
    is_main         = models.BooleanField(_("Is Option Main?"),default=False) 
    is_set          = models.BooleanField(_('Is set?'),default=False)
    option          = models.ForeignKey(Option, verbose_name=_("Option Value Parent Option"), on_delete=models.CASCADE, related_name='option')
    product         = models.ForeignKey(Product, verbose_name=_("Option Value Product"), on_delete=models.CASCADE,related_name='product_options')
    thumbnail       = models.ForeignKey(Image, verbose_name=_("Option Value Thumbnail"), on_delete=models.CASCADE,related_name='thumbnail')
    def __str__(self):
        return self.name + ' - ' + self.product.name

    class Meta:
        ordering=['-is_main']

