from peewee import *
from taskscron.msconnect import dbhandle


class Modelss(Model):
    class Meta:
        database = dbhandle
        db_table = "dsstore_modelss"

    id = PrimaryKeyField(null=False)
    name = CharField(default='', max_length=50)
    brends = SmallIntegerField(default=0)
    season_id = SmallIntegerField(default=0)
    price = FloatField(default=0.0)
    wholesale_price =FloatField(default=0)
    purshase_price =FloatField(default=0)
    description = TextField(default='')
    caption = CharField(default='', max_length=200)
    color = CharField(max_length=100, default='')
    discount = SmallIntegerField(default=0)
    sale = BooleanField(default=False)
    sale_price = FloatField(default=0)
    sale_date_end = DateTimeField()
    seo_attributes = TextField(default='')
    is_belarus = BooleanField(default=False)
    is_active = BooleanField(default=False)
    is_new = BooleanField(default=False)
    is_new_date_end = DateField()
    link_name = CharField(max_length=550)
    identifier = CharField(max_length=20)
    dirname_img = CharField(max_length=25, default='')
    date_create = DateTimeField()


class Products(Model):
    class Meta:
        database = dbhandle
        db_table = "dsstore_products"

    id = PrimaryKeyField(null=False)
    name = CharField(default='', max_length=50)
    brends = SmallIntegerField(default=0)
    season_id = SmallIntegerField(default=0)
    price = FloatField(default=0.0)
    wholesale_price =FloatField(default=0)
    purshase_price =FloatField(default=0)
    description = TextField(default='')
    caption = CharField(default='', max_length=200)
    color = CharField(max_length=100, default='')
    discount = SmallIntegerField(default=0)
    sale = BooleanField(default=False)
    sale_price = FloatField(default=0)
    sale_date_end = DateTimeField()
    seo_attributes = TextField(default='')
    is_belarus = BooleanField(default=False)
    is_active = BooleanField(default=False)
    is_new = BooleanField(default=False)
    is_new_date_end = DateField()
    link_name = CharField(max_length=550)
    identifier = CharField(max_length=20)
    dirname_img = CharField(max_length=25, default='')
    date_create = DateTimeField()