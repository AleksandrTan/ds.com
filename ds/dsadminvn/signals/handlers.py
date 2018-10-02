# from django.db.models.signals import post_save
# from django.dispatch import receiver
#
# from dsstore.models import Modelss, Products
#
#
# @receiver(post_save, sender=Modelss)
# def update_products(sender, instance, **kwargs):
#     products_list = instance.products_set.all()
#     for product in products_list:
#         product.discount = instance.discount
#         product.save()
