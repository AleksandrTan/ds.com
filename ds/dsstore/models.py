#from django.conf import settings
from django.db import models
from django.forms import ModelForm

from dsstore.mainhelpers import MainImgTypeField as MI


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

    class Meta:
        ordering = ['id']


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

    class Meta:
        ordering = ['id']

"""------------ SizeTable Model-------------------------------"""
class ManageSizeTable(models.Manager):

    def get_size_data(self, pk):
        return SizeTable.objects.filter(maincategory_id=pk).values('height')

class SizeTable(models.Model):
    maincategory = models.ForeignKey(MainCategory, on_delete=models.CASCADE)
    age = models.CharField(max_length=10, blank=False)
    height = models.SmallIntegerField(blank=False)
    chest = models.SmallIntegerField(blank=False)
    waist = models.SmallIntegerField(blank=False)
    objects = ManageSizeTable()

    class Meta:
        ordering = ['id']

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

    class Meta:
        ordering = ['id']

"""--------------------Seasons Model--------------------"""

class ManagerSeasons(models.Manager):
    def get_active_seasons(self):
        return Seasons.objects.filter(is_active__exact = True)

    def get_all_seasons(self):
        return Seasons.objects.all()

    def save_new_season(self, name, name_url):
        new_se = Seasons(name=name, name_url=name_url)
        new_se.save()
        return new_se

    def change_active_status(self, pk):
        se = Seasons.objects.get(pk=pk)
        if se.is_active:
            se.is_active = False
            data = {"status": False}
        else:
            se.is_active = True
            data = {"status": True}
        se.save()
        return data

class Seasons(models.Model):
    name = models.CharField(max_length=100)
    name_url = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    objects = ManagerSeasons()

    def get_absolute_url(self):
        return "/%s/" % self.name_url

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']


"""--------------Products Model-------------------------"""

def custom_directory_path(instance, filename):
    return 'images/{0}/{1}'.format(instance.dirname_img, filename)

class ManageProductsModel(models.Manager):

    def get_list_products(self):
        return Products.objects.only('id', 'articul', 'price', 'is_active')

    def check_iset_articul(self, articul):
        try:
            Products.objects.get(articul=articul)
            return True
        except Products.DoesNotExist:
            return False

class Products(models.Model):
    maincategory = models.ForeignKey(MainCategory, on_delete=models.CASCADE, blank=False)
    articul = models.CharField(unique=True, max_length=10, blank=False)
    nameproduct = models.ForeignKey(NameProduct, on_delete=models.CASCADE, blank=False)
    brends = models.SmallIntegerField(blank=True, default=0)
    season_id = models.SmallIntegerField(blank=True, default=0)
    price = models.FloatField(blank=True, default=0.0)
    wholesale_price = models.FloatField(blank=True, default=0)
    purshase_price = models.FloatField(blank=True, default=0)
    # main_photo_path = models.ImageField(blank=True, upload_to='images/')
    main_photo_path = MI.MainImgTypeField(upload_to=custom_directory_path,
                                          content_types=['image/jpg', 'image/png', 'image/jpeg'],
                                          max_upload_size=5000000, blank=True, default='nophoto.png')
    description = models.TextField(blank=True, default='')
    caption = models.CharField(blank=False, default='', max_length=200)
    color = models.CharField(max_length=100, blank=True, default='')
    discount = models.SmallIntegerField(blank=True, default=0)
    price_down = models.SmallIntegerField(blank=True, default=0)
    sale = models.BooleanField(default=False)
    sale_price = models.FloatField(default=0, blank=True)
    empty_count = models.BooleanField(default=False)
    seo_attributes = models.TextField(blank=True, default='')
    is_belarus = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)
    is_new_date_end = models.DateField(auto_now_add=True)
    link_name = models.CharField(max_length=550)
    identifier = models.CharField(max_length=20)
    dirname_img = models.CharField(max_length=25, default='', blank=True)
    date_create = models.DateTimeField(auto_now_add=True)
    objects = ManageProductsModel()

    def get_absolute_url(self):
        return "products/%s" % self.articul


    def __str__(self):
        return self.link_name

class ProductsForm(ModelForm):
    class Meta:
        model = Products
        fields = ['maincategory', 'articul', 'nameproduct', 'brends', 'season_id', 'price', 'wholesale_price', 'purshase_price', 'description',
                  'color', 'seo_attributes', 'main_photo_path', 'is_belarus', 'is_active', 'is_new', 'caption']

        error_messages = {
                             'articul': {'required': "Пожалуйста введите артикул",
                                         'max_length':"Не более 30 символов",
                                         'unique': "Этот артикул уже используетсяб введите другой"
                              },
                         }

"""--------------SizeCount Model--------------------------"""

class ManagerSizeCount(models.Manager):
    pass

class SizeCount(models.Model):
    products = models.ForeignKey(Products, on_delete=models.CASCADE)
    size = models.SmallIntegerField(default=0)
    count_num = models.SmallIntegerField(default=0)

    objects = ManagerSizeCount()


"""------------------Images Model---------------------------"""

class Image(models.Model):

    products = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='image')
    img_path = models.CharField(max_length=250, blank=True)

    def get_absolute_url(self):
        return self.img_path