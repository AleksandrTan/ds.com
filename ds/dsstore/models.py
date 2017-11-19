from django.db import models
from django.forms import ModelForm


"""-------------Main Category model--------------------"""

class ManagerMainCategories(models.Manager):
#Get active Categories
    def get_active_categories(self):
        return MainCategory.objects.filter(is_active__exact = True)


class MainCategory(models.Model):
    name = models.CharField(max_length=100)
    name_url = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    objects = ManagerMainCategories()

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
    age = models.CharField(max_length=10, blank=False)
    height = models.SmallIntegerField(blank=False)
    chest = models.SmallIntegerField(blank=False)
    waist = models.SmallIntegerField(blank=False)

class SizeTableForm(ModelForm):
    class Meta:
        model = SizeTable
        fields = ['age', 'height', 'chest', 'waist']
        error_messages = {
                            'age': {'required': "Пожалуйста введите возраст",
                                    'max_length': "Не более 10 символов"
                                      },
                            'height': {'required': "Пожалуйста введите рост",
                                       'max_length': "Не более 10 символов"
                                        },
                            'chest': {'required': "Пожалуйста введите обхват груди",
                                      'max_length': "Не более 10 символов"
                                            },
                            'waist': {'required': "Пожалуйста введите обхват талии",
                                      'max_length': "Не более 10 символов"},

                        }
