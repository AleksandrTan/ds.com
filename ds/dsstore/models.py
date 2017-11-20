from django.db import models
from django.forms import ModelForm


"""-------------Main Category model--------------------"""

class ManagerMainCategories(models.Manager):
#Get active Categories
    def get_active_categories(self):
        return MainCategory.objects.filter(is_active__exact = True)

    def get_all_categories(self):
        return MainCategory.objects.all()

    def save_new_category(self, name, name_url):
        new_mc = MainCategory(name=name, name_url=name_url)
        new_mc.save()
        return new_mc

    def change_active_status(self, pk):
        mc = MainCategory.objects.get(pk=pk)
        if mc.is_active:
            mc.is_active = False
            data = {"status": False}
        else:
            mc.is_active = True
            data = {"status": True}
        mc.save()
        return data

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
class ManagerNameProducts(models.Manager):
#Get active Categories
    def get_active_products(self):
        return NameProduct.objects.filter(is_active__exact = True)

    def get_all_products(self):
        return NameProduct.objects.all()

    def save_new_nameproduct(self, name, name_url):
        new_np = NameProduct(name=name, name_url=name_url)
        new_np.save()
        return new_np

    def change_active_status(self, pk):
        np = NameProduct.objects.get(pk=pk)
        if np.is_active:
            np.is_active = False
            data = {"status": False}
        else:
            np.is_active = True
            data = {"status": True}
        np.save()
        return data

class NameProduct(models.Model):
    name = models.CharField(max_length=100)
    name_url = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    objects = ManagerNameProducts()

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
        fields = ['age', 'height', 'chest', 'waist', 'maincategory']
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

"""-------------------Brends Model ------------------------------------"""
class ManagerBrends(models.Manager):

    def get_active_brends(self):
        return Brends.objects.filter(is_active__exact = True)

    def get_all_brends(self):
        return Brends.objects.all()

    def save_new_brend(self, name, name_url):
        new_br = Brends(name=name, name_url=name_url)
        new_br.save()
        return new_br

    def change_active_status(self, pk):
        br = Brends.objects.get(pk=pk)
        if br.is_active:
            br.is_active = False
            data = {"status": False}
        else:
            br.is_active = True
            data = {"status": True}
        br.save()
        return data

class Brends(models.Model):
    name = models.CharField(max_length=100)
    name_url = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    objects = ManagerBrends()

    def get_absolute_url(self):
        return "/%s/" % self.name_url

    def __str__(self):
        return self.name