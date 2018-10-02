from django.dispatch import receiver
from dsstore.models import Modelss, Products
from .signal import model_update


@receiver(model_update, sender=Modelss)
def update_products(sender, instance, **kwargs):
    products_list = instance.products_set.all()
    for product in products_list:
        Products.objects.update_product(product, instance)