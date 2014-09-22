from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.related import ForeignKey, ManyToManyField
from django.db.models import Model
from django.db.models.fields import CharField, DateTimeField, FloatField, IntegerField
from django.utils.translation import ugettext_lazy as _
# Create your models here.



class MyProfile(Model):
    id = IntegerField(verbose_name=_('owner'), primary_key=True, null=False, blank=False)
    speed_army = IntegerField(verbose_name=_('speed army'), unique=True, blank=False, null=False)
    speed_captain = IntegerField(verbose_name=_('speed captain'), unique=True, blank=False, null=False)
    speed_merchant = IntegerField(verbose_name=_('speed merchant'), unique=True, blank=False, null=False)
    speed_monk = IntegerField(verbose_name=_('speed monk'), unique=True, blank=False, null=False)