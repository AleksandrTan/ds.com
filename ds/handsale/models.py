from django.db import models
from django.forms import ModelForm

from dsstore.models import Products, SizeCount
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

"""-------------------- Model ProductSale--------------------------"""

class ManagerProductSale(models.Manager):
    pass

class ProductsSale(models.Model):
    products = models.ForeignKey(Products, on_delete=models.SET_NULL, related_name='psale', null=True, blank=True)
    articul = models.CharField(max_length=10, blank=False)
    count_num = models.SmallIntegerField(default=0, blank=False)
    size = models.SmallIntegerField(default=0, blank=False)
    price = models.FloatField(blank=False, default=0.0)
    lost_num = models.FloatField(blank=True, default=0.0)
    plase_sale = models.SmallIntegerField(blank=False, default=1)
    date_sale = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='productssale', null=True, blank=True)
    link_name = models.CharField(max_length=550)
    order_status = models.SmallIntegerField(default=4, blank=False)
    declaration_number = models.CharField(default='', blank=True, max_length=50)
    date_send = models.DateField(blank=False)
    is_return = models.BooleanField(default=False)
    date_return = models.DateField(blank=False)
    description = models.CharField(default='', blank=True, max_length=2000)
    objects = ManagerProductSale()

class ProductsSellForm(ModelForm):
    class Meta:
        model = ProductsSale
        fields = ['size', 'products', 'count_num', 'price', 'lost_num', 'description']

        error_messages = {
            'count_num': {'required': "Пожалуйста введите колличество"}
        }

    def clean(self):
        # check the quantity of goods sold and availability in stock
        cleaned_data = self.cleaned_data
        sizecount = SizeCount.objects.get_single_sizecount(cleaned_data['size'])
        if cleaned_data.get("count_num") > sizecount.count_num:
            raise ValidationError('Колличество продаваемого товара больше чем на складе!!!', code='invalid')
        return self.cleaned_data