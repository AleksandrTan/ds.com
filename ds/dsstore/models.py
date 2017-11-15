from django.db import models


"""-------------Main Category model--------------------"""

class MainCategory(models.Model):
    name = models.CharField(max_length=100)
    name_url = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def get_absolute_url(self):
        return "/%s/" % self.name_url

    def __str__(self):
        return self.name


"""----------- Name Producn model -----------------------"""

class NameProduct(models.Model):
    name = models.CharField(max_length=100)
    name_url = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def get_absolute_url(self):
        return "/%s/" % self.name_url

    def __str__(self):
        return self.name

"""------------ SizeTable Model-------------------------------"""

class SizeTable(models.Model):
    maincategory = models.ForeignKey(MainCategory, on_delete=models.CASCADE)
    age = models.CharField(max_length=100)
    height = models.SmallIntegerField()
    chest = models.SmallIntegerField()
    waist = models.SmallIntegerField()