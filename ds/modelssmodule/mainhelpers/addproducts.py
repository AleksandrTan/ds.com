from dsstore.models import ProductsAddFormModelss
from dsadminvn.mainhelpers.SetBarcode import SetBarcode


class AddProducts:
    def __init__(self, instance, pr_data):
        self.instance = instance
        self.pr_data = pr_data
        self.error_list = list()
        self.data = dict()

    def saved_products(self):
        import json
        products_dict = json.loads(self.pr_data)
        self.data['modelss'] = self.instance.id
        for product in products_dict:
            self.save_product(products_dict[product], self.data)
        if self.error_list:
            return self.error_list
        else:
            return False

    def save_product(self, product, data):
        data['articul'] = product['articul']
        data['pre_barcode'] = product['barcode']
        data['count_num'] = int(product['count'])
        data['size'] = int(product['height'])
        genbarcode = SetBarcode(product['barcode'])
        data['barcode'] = genbarcode.generate_barcode()
        data['main_photo_path'] = self.instance.main_photo_path
        data['modelss_name'] = self.instance.name
        data['maincategory'] = self.instance.maincategory_id
        data['dirname_img'] = self.instance.dirname_img
        data['identifier'] = self.uuid_sentece_user()
        data['discount'] = self.instance.discount
        data['nameproduct'] = self.instance.nameproduct_id
        data['brends'] = self.instance.brends
        data['season_id'] = self.instance.season_id
        data['wholesale_price'] = self.instance.wholesale_price
        data['purshase_price'] = self.instance.purshase_price
        data['description'] = self.instance.description
        data['color'] = self.instance.color
        data['seo_attributes'] = self.instance.seo_attributes
        data['is_belarus'] = self.instance.is_belarus
        data['is_active'] = self.instance.is_active
        data['is_new'] = self.instance.is_new
        data['caption'] = self.instance.caption
        data['sale_price'] = self.instance.sale_price
        data['price_down'] = self.instance.price_down
        data['price'] = self.instance.price
        form = ProductsAddFormModelss(data)
        if form.is_valid():
           form.save()
        else:
            self.error_list.append(form.errors)

    def uuid_sentece_user(self):
        import uuid
        return 'product_' + str(uuid.uuid4())[:10]