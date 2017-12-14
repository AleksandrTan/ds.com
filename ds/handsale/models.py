from django.db import models
from django.forms import ModelForm

from dsstore.models import Products
from django.contrib.auth.models import User

"""-------------------- Model ProductSale--------------------------"""

class ManagerProductSale(models.Manager):
    pass

class ProductsSale(models.Model):
    products = models.ForeignKey(Products, on_delete=models.SET_NULL, related_name='psale', null=True, blank=True)
    articul = models.CharField(max_length=10, blank=False)
    count_num = models.SmallIntegerField(default=0)
    size = models.SmallIntegerField(default=0)
    price = models.FloatField(blank=False, default=0.0)
    place_sale = models.SmallIntegerField(blank=False, default=1)
    date_sale = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='productssale', null=True, blank=True)
    link_name = models.CharField(max_length=550)
    order_status = models.SmallIntegerField(default=1, blank=True)
    declaration_number = models.CharField(default='', blank=True, max_length=150)
    date_send = models.DateField(blank=False)
    is_return = models.BooleanField(default=False)
    date_return = models.DateField(blank=False)
    objects = ManagerProductSale()
