from django.dispatch import Signal
#signal for update products when updating model
model_update = Signal(providing_args=['instance'])