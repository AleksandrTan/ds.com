from django.db import models

"""-------------Main Category model--------------------"""

class MainCategory(models.Model):
    name = models.CharField(max_length=100)
    name_url = models.CharField(max_length=100)
    is_active =models.BooleanField(default=True)