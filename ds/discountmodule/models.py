from django.db import models


class DiscountsManager(models.Manager):
    def get_list_discounts(self):
        return Discounts.objects.only('id', 'my_description', 'description', 'date_create')


class Discounts(models.Model):
    list_id = models.TextField()
    my_description = models.CharField(max_length=2000)
    description = models.CharField(max_length=2000)
    date_create = models.DateTimeField(auto_now_add=True)
    disco_value = models.SmallIntegerField(blank=True, default=0)
    objects = DiscountsManager()