from django.db import models


class DiscountsManager(models.Manager):

    def get_list_discounts(self):
        return Discounts.objects.only('id', 'my_description', 'description', 'date_create', 'disco_value')

    def save_discount(self, list_id, description, disco_value, sale_date_end):
        Discounts(list_id=list_id, my_description='', description=description, disco_value=disco_value, sale_date_end=sale_date_end).save()


class Discounts(models.Model):
    list_id = models.TextField()
    my_description = models.CharField(max_length=2000)
    description = models.CharField(max_length=2000)
    date_create = models.DateTimeField(auto_now_add=True)
    disco_value = models.SmallIntegerField(blank=True, default=0)
    sale_date_end = models.DateTimeField()
    objects = DiscountsManager()