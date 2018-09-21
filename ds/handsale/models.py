from datetime import datetime
from datetime import date

from django.db import models
from django.db.models import Sum
from django.forms import ModelForm
from django.forms import modelformset_factory

from dsstore.models import Products, SizeCount
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

"""-------------------- Model ProductSale--------------------------"""


class ManagerProductSale(models.Manager):

    def return_sale(self, pk, pk_product):
        psale = ProductsSale.objects.filter(id=pk).get()
        psale.is_return = True
        psale.date_return = datetime.now()
        psale.total_amount = 0.0
        psale.order_status = 5
        # psale.price = 0
        # psale.true_price = 0
        # psale.lost_num = 0
        # psale.count_num = 0
        psale.save()
        Products.objects.return_amount(pk_product)

    def get_list_data(self, products_id, data={}):
        if data:
            return self.filter_date_sales(products_id, data)
        else:
            return ProductsSale.objects.filter(products_id=products_id)

    def filter_date_sales(self, products_id, data={}):
        query = ProductsSale.objects
        if data['date_with'] and data['date_by']:
            return query.filter(date_sale__gte=data['date_with']).filter(date_sale__lte=data['date_by']).filter(products_id=products_id)

    def day_statistics_sales(self):
        return ProductsSale.objects.filter(date_sale=date.today()).filter(is_return=False)

    def day_statistics_returns(self):
        return ProductsSale.objects.filter(date_sale=date.today()).filter(is_return=True)

    def sum_sales_day(self):
        return ProductsSale.objects.filter(date_sale=date.today()).filter(is_return=False).all().aggregate(price_per_page=Sum('true_price'))

    def sum_returns_day(self):
        return ProductsSale.objects.filter(date_sale=date.today()).filter(is_return=True).all().aggregate(price_per_page=Sum('true_price'))

    def filterstat_date_sales(self, data=dict()):
        if data:
            return ProductsSale.objects.filter(date_sale__gte=data['date_with']).filter(date_sale__lte=data['date_by']).filter(is_return=False).\
                all().aggregate(price_per_page=Sum('true_price'))
        else:
            return ProductsSale.objects.filter(date_sale__gte=date.today()).filter(date_sale__lte=date.today()).filter(is_return=False).\
                all().aggregate(price_per_page=Sum('true_price'))

    def filterstat_date_return(self, data=dict()):
        if data:
            return ProductsSale.objects.filter(date_sale__gte=data['date_with']).filter(date_sale__lte=data['date_by']).filter(is_return=True).\
                all().aggregate(price_per_page=Sum('true_price'))
        else:
            return ProductsSale.objects.filter(date_sale__gte=date.today()).filter(date_sale__lte=date.today()).filter(is_return=True).\
                all().aggregate(price_per_page=Sum('true_price'))


class ProductsSale(models.Model):
    products = models.ForeignKey(Products, on_delete=models.SET_NULL, related_name='psale', null=True, blank=True)
    articul = models.CharField(max_length=10, blank=False)
    count_num = models.SmallIntegerField(default=1, blank=False)
    size = models.SmallIntegerField(default=0, blank=False)
    price = models.FloatField(blank=False, default=0.0)
    true_price = models.FloatField(blank=False, default=0.0)
    purshase_price = models.FloatField(blank=True, default=0.0)
    total_amount = models.FloatField(blank=False, default=0.0)
    lost_num = models.FloatField(blank=True, default=0.0)
    plase_sale = models.SmallIntegerField(blank=False, default=1)
    discount = models.SmallIntegerField(blank=True, default=0)
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

    def get_absolute_url(self):
        return "products/%s" % self.link_name

    def __str__(self):
        return self.link_name


class ProductsSellForm(ModelForm):

    class Meta:
        model = ProductsSale
        fields = ['size', 'products', 'count_num', 'price', 'lost_num', 'description']

        error_messages = {
            'count_num': {'required': "Пожалуйста введите колличество"},
            'price': {'invalid': "Для товара не указана цена"}
        }

    def clean(self):
        # check the quantity of goods sold and availability in stock
        cleaned_data = self.cleaned_data
        product = Products.objects.get_single_product(cleaned_data['products'].id)
        if cleaned_data.get("count_num") and cleaned_data.get("count_num") > product.count_num:
            raise ValidationError('Колличество продаваемого товара больше чем на складе!!!', code='invalid')
        return self.cleaned_data

ProductsBarcodeFormSet = modelformset_factory(ProductsSale, fields=('products', 'lost_num', 'description'))