from django.dispatch import Signal

model_update = Signal(providing_args=['instance'])