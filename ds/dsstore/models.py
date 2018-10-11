from django.db.models import F
from django.db import models
from django.forms import ModelForm
from django.core.exceptions import ValidationError

from dsstore.mainhelpers import MainImgTypeField as MI

"""-------------Main Category model--------------------"""


class ManagerMainCategories(models.Manager):
#Get active Categories
    def get_active_categories(self):
        return MainCategory.objects.filter(is_active__exact=True)

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

    def get_single_maincategory(self, pk):
        try:
            return MainCategory.objects.get(id=pk)
        except Products.DoesNotExist:
            return False


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
        ordering = ['height']


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


"""-------------------------Modelss Model---------------------"""


def custom_directory_path(instance, filename):
    return 'images/{0}/{1}'.format(instance.dirname_img, filename)


class ManageModelss(models.Manager):

    def check_isset_modelss(self, name):
        if Modelss.objects.only('name').filter(name=name).exists():
            return True
        else:
            return False

    def get_list_products(self):
        return Modelss.objects.only('id', 'price', 'is_active', 'name')

    def found_modelss(self, name):
        try:
            return Modelss.objects.filter(name=name).get()
        except Modelss.DoesNotExist:
            return False

    def filter_modelss(self, data):
        query = Modelss.objects
        work_dict = {param: data[param] for param in data if data[param]}
        try:
            return query.filter(**work_dict)
        except Modelss.DoesNotExist:
            return False

    def get_modelss(self, pk):
        try:
            return Modelss.objects.filter(id=pk).get()
        except Modelss.DoesNotExist:
            return False

    def get_modelss_id(self, name):
        try:
            return Modelss.objects.filter(name=name).values_list('id', flat=True)
        except Modelss.DoesNotExist:
            return False

    def set_discount_models(self, data, disco_value):
        query = Modelss.objects
        work_dict = {param: data[param] for param in data if data[param]}
        try:
            count_record = query.filter(**work_dict).update(discount=disco_value)
            if count_record > 0:
                return ','.join([str(i) for i in query.filter(**work_dict).values_list('id', flat=True)])
            else:
                return False
        except Modelss.DoesNotExist:
            return False

    def set_sales_models(self, data, disco_value):
        query = Modelss.objects
        work_dict = {param: data[param] for param in data if data[param]}
        try:
            count_record = query.filter(**work_dict).update(discount=disco_value, sale=True, sale_price=F('price') - ((F('price')*disco_value)/100))
            if count_record > 0:
                return ','.join([str(i) for i in query.filter(**work_dict).values_list('id', flat=True)])
            else:
                return False
        except Modelss.DoesNotExist:
            return False

    def set_discount_model_products(self, name, disco_value):
        try:
            count_record = Modelss.objects.filter(name=name).update(discount=disco_value)
            if count_record > 0:
                return str(Modelss.objects.get_modelss_id(name)[0])
            else:
                return False
        except Products.DoesNotExist:
            return False

    def delete_discount(self, id_list):
        Modelss.objects.filter(id__in=id_list).update(discount=0, sale=False, sale_price=0)


class Modelss(models.Model):
    name = models.CharField(blank=False, default='', max_length=50)
    maincategory = models.ForeignKey(MainCategory, on_delete=models.CASCADE, blank=False)
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
    sale = models.BooleanField(default=False)
    sale_price = models.FloatField(default=0, blank=True)
    seo_attributes = models.TextField(blank=True, default='')
    is_belarus = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)
    is_new_date_end = models.DateField(auto_now_add=True)
    link_name = models.CharField(max_length=550)
    identifier = models.CharField(max_length=20)
    dirname_img = models.CharField(max_length=25, default='', blank=True)
    date_create = models.DateTimeField(auto_now_add=True)
    objects = ManageModelss()

    # change the main_imgfield value to be the newley modifed image value - png
    # def clean(self):
    #     from PIL import Image as Ima
    #     from io import BytesIO
    #     from django.core.files.uploadedfile import InMemoryUploadedFile
    #     import sys
    #     # Opening the uploaded image
    #     im = Ima.open(self.main_photo_path)
    #     output = BytesIO()
    #     # Resize/modify the image
    #     im = im.resize((277, 205))
    #     # after modifications, save it to the output
    #     im.save(output, format='PNG', quality=100)
    #     output.seek(0)
    #
    #     # change the main_imgfield value to be the newley modifed image value - png
    #     self.main_photo_path = InMemoryUploadedFile(output, 'MI.MainImgTypeField', "%s.png" % self.main_photo_path.name.split('.')[0],
    #                                          'image/png', sys.getsizeof(output), None)
    #     super(Products, self).clean()

    def get_absolute_url(self):
         return "products/%s" % self.link_name

    def __str__(self):
        return self.link_name


class ModelssForm(ModelForm):
    """
        Set request param, param request add  in __init__ like positional argument
    """
    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(ModelForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Modelss
        fields = ['maincategory', 'nameproduct', 'brends', 'season_id', 'price', 'wholesale_price', 'purshase_price', 'description',
                  'color', 'seo_attributes', 'main_photo_path', 'is_belarus', 'is_active', 'is_new', 'caption', 'name']

        error_messages = {
                             'name': {'required': "Пожалуйста введите название",
                                      'max_length':"Не более 30 символов",
                                      'unique': "Эта модель уже используетсяб введите другую"
                                      },
                             'caption': {
                                      'required': "Пожалуйста введите заголовок",
                             }
                          }


class ModelssFormEdit(ModelForm):
    """
        Set request param, param request add  in __init__ like positional argument for clean method
    """
    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(ModelForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Modelss
        fields = ['nameproduct', 'brends', 'season_id', 'price', 'wholesale_price', 'purshase_price', 'description',
                  'color', 'seo_attributes', 'main_photo_path', 'is_belarus', 'is_active', 'is_new', 'caption', 'name', 'discount']

        error_messages = {
                             'caption': {
                                      'required': "Пожалуйста введите заголовок",
                             }
                          }

"""--------------Products Model-------------------------"""


class ManageProductsModel(models.Manager):

    def get_list_products(self):
        return Products.objects.only('id', 'articul', 'price', 'is_active')

    def check_isset_articul(self, articul, flag_isset=False):
        try:
            product = Products.objects.only('articul').get(articul=articul)
            if flag_isset:
                return product.articul
            else:
                return True
        except Products.DoesNotExist:
            return False

    def check_isset_pre_barcode(self, pre_barcode, flag_isset=False):
        try:
            product = Products.objects.only('pre_barcode').get(pre_barcode=pre_barcode)
            if flag_isset:
                return product.pre_barcode
            else:
                return True
        except Products.DoesNotExist:
            return False

    def found_articul(self, articul):
        try:
            return Products.objects.get(articul=articul)
        except Products.DoesNotExist:
            return False

    def filter_products(self, data):
        query = Products.objects
        work_dict = {param: data[param] for param in data if data[param]}
        try:
            return query.filter(**work_dict)
        except Products.DoesNotExist:
            return False

    def get_single_product(self, pk):
        try:
            return Products.objects.get(id=pk)
        except Products.DoesNotExist:
            return False

    def get_product_barcode(self, barcode):
        # if get articul
        if len(barcode) < 13 and len(barcode) != 0:
            try:
                product = Products.objects.filter(articul=barcode).only('articul', 'barcode', 'price', 'discount', 'size').get()
                if product.price:
                    return {'status': True, 'data_product': self.hm_get_barcode_query(product)}
                else:
                    return {'status': False}

            except Products.DoesNotExist:
                return {'status': False}
        # if get barcode
        elif len(barcode) == 13:
            try:
                product = Products.objects.filter(barcode=barcode).only('articul', 'barcode', 'price', 'discount', 'size').get()
                if product.price:
                    return {'status': True, 'data_product': self.hm_get_barcode_query(product)}
                else:
                    return {'status': False}
            except Products.DoesNotExist:
                return {'status': False}
        else:
            return {'status': False}

    def reduce_amount(self, pk, count_num=0):
        try:
            size = Products.objects.only("size").get(id=pk)
            # reduce the amount of goods for a size
            size.count_num = size.count_num - count_num
            size.save()
            return size.size
        except Products.DoesNotExist:
            return False

    def return_amount(self, pk):
        try:
            size = Products.objects.only("size").get(id=pk)
            # reduce the amount of goods for a size
            size.count_num = size.count_num + 1
            size.save()
            return size.size
        except Products.DoesNotExist:
            return False

    def set_discount_products(self, list_mid, disco_value):
        try:
            Products.objects.filter(modelss_id__in=list_mid.split(',')).update(discount=disco_value)
        except Products.DoesNotExist:
            return False

    def set_discount_model_products(self, modelss, disco_value):
        try:
            count_record = Products.objects.filter(modelss=modelss).update(discount=disco_value)
            if count_record > 0:
                return ','.join([str(i) for i in Products.objects.filter(modelss=modelss).values_list('id', flat=True)])
            else:
                return False
        except Products.DoesNotExist:
            return False

    def set_sales_products(self, list_mid, disco_value):
        try:
            Products.objects.filter(modelss_id__in=list_mid.split(',')).update(discount=disco_value, sale=True,
                                                                               sale_price=F('price') - ((F('price')*disco_value)/100))
        except Products.DoesNotExist:
            return False

    def delete_discount(self, list_mid):
        Products.objects.filter(modelss_id__in=list_mid).update(discount=0, sale=False, sale_price=0)

    def hm_get_barcode_query(self, product):
        data_product = dict()
        data_product['id'] = product.id
        data_product['articul'] = product.articul
        data_product['barcode'] = product.barcode
        data_product['price'] = product.price
        data_product['discount'] = product.discount
        data_product['price_discount'] = product.price if product.discount == 0 else \
            product.price - ((product.price * product.discount) / 100)
        data_product['category'] = product.maincategory.name
        data_product['name'] = product.nameproduct.name
        data_product['size'] = product.size
        return data_product

    def update_product(self, product, instance):
        product.discount = instance.discount
        product.nameproduct = instance.nameproduct
        product.brends = instance.brends
        product.season_id = instance.season_id
        product.wholesale_price = instance.wholesale_price
        product.purshase_price = instance.purshase_price
        product.description = instance.description
        product.color = instance.color
        product.seo_attributes = instance.seo_attributes
        product.main_photo_path = instance.main_photo_path
        product.is_belarus = instance.is_belarus
        product.is_active = instance.is_active
        product.is_new = instance.is_new
        product.caption = instance.caption
        product.sale_price = instance.sale_price
        product.save()


class Products(models.Model):
    maincategory = models.ForeignKey(MainCategory, on_delete=models.CASCADE, blank=False)
    articul = models.CharField(unique=True, max_length=10, blank=False)
    pre_barcode = models.CharField(unique=True, max_length=5, blank=False)
    barcode = models.CharField(unique=True, max_length=13, blank=False)
    nameproduct = models.ForeignKey(NameProduct, on_delete=models.CASCADE, blank=False)
    brends = models.SmallIntegerField(blank=True, default=0)
    season_id = models.SmallIntegerField(blank=True, default=0)
    price = models.FloatField(blank=True, default=0.0)
    wholesale_price = models.FloatField(blank=True, default=0)
    purshase_price = models.FloatField(blank=True, default=0)
    modelss = models.ForeignKey(Modelss, on_delete=models.CASCADE, blank=False)
    modelss_name = models.CharField(blank=True, default='', max_length=50)
    size = models.SmallIntegerField(blank=True, default=0)
    count_num = models.SmallIntegerField(blank=True, default=0)
    main_photo_path = models.CharField(max_length=250, blank=True)
    description = models.TextField(blank=True, default='')
    caption = models.CharField(blank=False, default='', max_length=200)
    color = models.CharField(max_length=100, blank=True, default='')
    discount = models.SmallIntegerField(blank=True, default=0)
    sale = models.BooleanField(default=False)
    sale_price = models.FloatField(default=0, blank=True)
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

    # change the main_imgfield value to be the newley modifed image value - png
    # def clean(self):
    #     from PIL import Image as Ima
    #     from io import BytesIO
    #     from django.core.files.uploadedfile import InMemoryUploadedFile
    #     import sys
    #     # Opening the uploaded image
    #     im = Ima.open(self.main_photo_path)
    #     output = BytesIO()
    #     # Resize/modify the image
    #     im = im.resize((277, 205))
    #     # after modifications, save it to the output
    #     im.save(output, format='PNG', quality=100)
    #     output.seek(0)
    #
    #     # change the main_imgfield value to be the newley modifed image value - png
    #     self.main_photo_path = InMemoryUploadedFile(output, 'MI.MainImgTypeField', "%s.png" % self.main_photo_path.name.split('.')[0],
    #                                          'image/png', sys.getsizeof(output), None)
    #     super(Products, self).clean()

    def get_absolute_url(self):
         return "products/%s" % self.link_name

    def __str__(self):
        return self.link_name


class ProductsForm(ModelForm):
    """
        Set request param, param request add  in __init__ like positional argument
    """
    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(ProductsForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Products
        fields = ['maincategory', 'articul', 'nameproduct', 'brends', 'season_id', 'price', 'wholesale_price', 'purshase_price', 'description',
                  'color', 'seo_attributes', 'main_photo_path', 'is_belarus', 'is_active', 'is_new', 'caption', 'pre_barcode', 'modelss', 'size',
                  'count_num', 'modelss_name']

        error_messages = {
                             'articul': {'required': "Пожалуйста введите артикул",
                                         'max_length':"Не более 30 символов",
                                         'unique': "Этот артикул уже используетсяб введите другой"
                                         },
                             'pre_barcode': {'required': "Пожалуйста введите Штрих-код",
                                             'max_length': "Не более 5 символов",
                                             'unique': "Этот штрих-код уже используетсяб введите другой"
                                             },
                         }

    def clean(self):
        # check if count height's not moore sizes num for maincategory
        cleaned_data = self.cleaned_data
        maincategory = cleaned_data['maincategory']
        if len(self.request.POST.getlist('height[]')) > maincategory.sizetable_set.count():
            raise ValidationError('Колличество введенных размеров больше чем размеров категории', code='invalid')
        #check isset articul
        if Products.objects.check_isset_articul(cleaned_data['articul']):
            raise ValidationError('Введенный артикул уже существует!Выберите другой', code='invalid')
        #check 5 num in pre_barcode
        if len(cleaned_data['pre_barcode']) < 5:
            raise ValidationError ('Штрих-код должен содержать 5 цифр!!!')
        if not type(int(cleaned_data['pre_barcode'])) is int:
            raise ValidationError('Должны быть только цифры')
        # check isset pre_barcode
        if Products.objects.check_isset_pre_barcode(cleaned_data['pre_barcode']):
            raise ValidationError('Введенный штрих-код уже существует!Выберите другой', code='invalid')
        return self.cleaned_data


class ProductsFormEdit(ModelForm):
    """
        set request param, param request add  in __init__ like positional argument for check in clean method
        """
    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(ProductsFormEdit, self).__init__(*args, **kwargs)

    class Meta:
        model = Products
        fields = ['maincategory', 'articul', 'nameproduct', 'brends', 'season_id', 'price', 'wholesale_price', 'purshase_price', 'description',
                  'color', 'seo_attributes', 'main_photo_path', 'is_belarus', 'is_active', 'is_new', 'caption', 'discount',
                  'pre_barcode', 'modelss', 'size', 'count_num']

        error_messages = {
                             'articul': {'required': "Пожалуйста введите артикул",
                                         'max_length':"Не более 30 символов",
                                         'unique': "Этот артикул уже используетсяб введите другой"
                                         },
                             'pre_barcode': {'required': "Пожалуйста введите Штрих-код",
                                             'max_length': "Не более 5 символов",
                                             'unique': "Этот штрих-код уже используетсяб введите другой"
                                             },
                         }

    def clean(self):
        # check if count height's not moore sizes num for maincategory
        cleaned_data = self.cleaned_data
        maincategory = cleaned_data['maincategory']
        if len(self.request.POST.getlist('height[]')) > maincategory.sizetable_set.count():
            raise ValidationError('Колличество введенных размеров больше чем размеров категории', code='invalid')
        #check isset articul
        if self.request.POST.getlist('articul_product_hidden')[0] != cleaned_data['articul']:
            cleaned_data['articul'] = self.request.POST.getlist('articul_product_hidden')[0]
            raise ValidationError('Вы изменили существующий артикул!!!Нельзя так делать!!!', code='invalid')

        return self.cleaned_data


class ProductsFormModelss(ModelForm):

    class Meta:
        model = Products
        fields = ['maincategory', 'nameproduct', 'brends', 'season_id', 'price', 'wholesale_price', 'purshase_price', 'description',
                  'color', 'seo_attributes', 'is_belarus', 'is_active', 'is_new', 'caption', 'modelss', 'articul', 'pre_barcode',
                  'size', 'count_num', 'main_photo_path', 'modelss_name', 'dirname_img', 'identifier', 'barcode']


class ProductsAddFormModelss(ModelForm):

    class Meta:
        model = Products
        fields = ['maincategory', 'nameproduct', 'brends', 'season_id', 'price', 'wholesale_price', 'purshase_price', 'description',
                  'color', 'seo_attributes', 'is_belarus', 'is_active', 'is_new', 'caption', 'modelss', 'articul', 'pre_barcode',
                  'size', 'count_num', 'main_photo_path', 'modelss_name', 'dirname_img', 'identifier', 'barcode', 'discount']


""""--------------SizeCount Model--------------------------"""


class ManagerSizeCount(models.Manager):

    def get_single_size(self, pk, count_num=0):
        try:
            size = SizeCount.objects.only("size").get(id=pk)
            # reduce the amount of goods for a size
            size.count_num = size.count_num - count_num
            size.save()
            return size.size
        except Products.DoesNotExist:
            return False

    def get_single_sizecount(self, pk):
        try:
            return SizeCount.objects.get(id=pk)
        except Products.DoesNotExist:
            return False

    def return_product(self, products_id, size, count_num):
        order = SizeCount.objects.filter(products_id=products_id).filter(size=size).get()
        order.return_product(count_num)


class SizeCount(models.Model):
    products = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='sizecount', null=True)
    size = models.SmallIntegerField(default=0)
    count_num = models.SmallIntegerField(default=0)

    objects = ManagerSizeCount()

    def return_product(self, count_num):
        self.count_num += count_num
        self.save()

    class Meta:
        ordering = ['size']

"""------------------Images Model---------------------------"""


class Image(models.Model):

    modelss = models.ForeignKey(Modelss, on_delete=models.CASCADE, related_name='image')
    img_path = models.CharField(max_length=250, blank=True)

    def get_absolute_url(self):
        return self.img_path