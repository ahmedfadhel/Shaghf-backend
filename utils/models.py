from django.db import models
from django.utils.translation import gettext as _

# Create your models here.

class TimestampMixin(models.Model):
    created_at = models.DateField(_("Created At"),auto_now_add=True)
    updated_at = models.DateField(_("Updated At"), auto_now=True)
    class Meta:
        abstract = True
        