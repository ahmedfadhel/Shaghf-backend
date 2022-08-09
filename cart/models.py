from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.translation import gettext as _
from store.models import OptionValue

from utils.models import TimestampMixin

from .utils import generate_order_id


# Create your models here.
class ShippingInfo(TimestampMixin, models.Model):
    name = models.CharField(_("Shipping Name"), max_length=50,default='name')
    gover_options =(
        ('an','الانبار'),
        ('ba','بابل'),
        ('bg','بغداد'),
        ('bs','البصرة'),
        ('na','الناصرية'),
        ('di','الديوانية'),
        ('dy','ديالى'),
        ('dh','دهوك'),
        ('er','أربيل'),
        ('ha','الحلة'),
        ('ka','كربلاء'),
        ('ki','كركوك'),
        ('am','العمارة'),
        ('sa','السماوة'),
        ('nj','نجف'),
        ('mo','الموصل'),
        ('sa','صلاح الدين'),
        ('su','السليمانية'),
        ('ku','الكوت'),
    )

    gover = models.CharField(_("Governorate Name"), max_length=3,choices=gover_options)
    city = models.CharField(_("City Name"), max_length=50)
    phone = models.CharField(
    _("Shipping Phone Number"),
    max_length=16,
    
    validators=[
      RegexValidator(
        regex=r"^(((?:\+|00)964)|(0)*)7[578]\d{8}$",
        message="رقم الهاتف غير صحيح."
      ),
    ],
  )
    near_point = models.CharField(_("Nearset Point Name"), max_length=50)
    def __str__(self):
        return self.phone
    
class OrderItem(TimestampMixin,models.Model):
    
    # product = models.OneToOneField(OptionValue, verbose_name=_("Product"), on_delete=models.SET_NULL,null=True)
    product = models.ForeignKey(OptionValue, verbose_name=_("Product"), on_delete=models.SET_NULL,null=True)

    qty = models.IntegerField(_("Product Quentity"))
    price = models.IntegerField(_("Prodcut Price"),default=0)
    def __str__(self):
        return self.product.product.name

class Order(TimestampMixin,models.Model):
    order_status=(
        ('re','تم استلام الطلب'),
        ('pre','تم تجهيز الطلب'),
        ('sh','تم شحن الطلب'),
        ('de','تم تسليم الطلب'),
    )
    order_status = models.CharField(_("Order Status"), max_length=50,choices=order_status,default='re')
    ref_code = models.CharField(_("Order Id"), max_length=11)
    items = models.ManyToManyField(OrderItem)
    shipping = models.ForeignKey(ShippingInfo, verbose_name=_("Order Shipping Address"), on_delete=models.SET_NULL,null=True)
    # class Meta:
      # ordering=['-order_status']
    def __str__(self):
        return self.ref_code  
@receiver(pre_save,sender=Order)
def genreate_order_ref_code(sender, instance, *args, **kwargs):
    if(instance.pk is None):
      instance.ref_code = generate_order_id()