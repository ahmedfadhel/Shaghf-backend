from django.db import models
from utils.models import TimestampMixin
from django.utils.translation import gettext as _
from datetime import date,datetime
# Create your models here.
class Discount(TimestampMixin,models.Model):
    discount_option = (
        ('sh','shipping'),
        ('pr','price')
    )
    code = models.CharField(_("Discount Code"), max_length=50,unique=True)
    valid_from = models.DateField(_("Discount start date"))
    valid_to = models.DateField(_("Discount end date"))
    discount = models.FloatField(_("Discount Precentage"),default=0)
    discount_type = models.CharField(_("Discount_type"), max_length=2,choices=discount_option,default='pr')
    
    @property
    def is_active(self):
        return (self.valid_to >= date.today() and self.valid_from <= date.today())
    
    def __str__(self) :
        return self.code