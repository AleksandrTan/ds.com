from django.http import QueryDict
from dsstore.models import (Products, ProductsFormModelss)
from dsadminvn.mainhelpers.SetBarcode import SetBarcode


class SavedProducts:
    def __init__(self, instance, request):
        self.instance = instance
        self.request = request
        self.error_list = list()

    def saved_products(self):
        import json
        products_dict = json.loads(self.request.POST.getlist('product_data_lists')[0])
        self.request.POST['modelss'] = self.instance.id
        copy_get = self.request.POST.copy()
        copy_get.pop('articul[]')
        copy_get.pop('pre_barcode[]')
        copy_get.pop('count[]')
        copy_get.pop('height[]')
        for product in products_dict:
            self.save_product(products_dict[product], copy_get)
        if self.error_list:
            return self.error_list
        else:
            return True

    def save_product(self, product, data):
        data['articul'] = product['articul']
        data['pre_barcode'] = product['barcode']
        data['count_num'] = int(product['count'])
        data['size'] = int(product['height'])
        genbarcode = SetBarcode(product['barcode'])
        data['barcode'] = genbarcode.generate_barcode()
        data['main_photo_path'] = self.instance.main_photo_path
        data['modelss_name'] = self.request.POST.getlist('name')[0]
        data['dirname_img'] = self.instance.dirname_img
        data['identifier'] = self.uuid_sentece_user()
        form = ProductsFormModelss(data)
        if form.is_valid():
           form.save()
        else:
            self.error_list.append(form.errors)

    def uuid_sentece_user(self):
        import uuid
        return 'product_' + str(uuid.uuid4())[:10]