from peewee import *
from datetime import datetime
from taskscron.models import Modelss, Products, Discounts, DoesNotExist


class CheckSales:

    def __init__(self):
        self.endtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def get_sales(self):
        try:
            id_list = Discounts.select().where((Discounts.sale_date_end < self.endtime) & (Discounts.sale == 1))
            if id_list:
                self.check_discounts(id_list)
        except DoesNotExist:
            pass

    def check_discounts(self, id_list):
        for records in id_list:
            # print(records.id)
            if records.list_id:
                id_models = records.list_id.split(',')
                self.check_sales_modelss(id_models)
                self.check_sales_products(id_models)
                records.delete().execute()
            else:
                continue

    def check_sales_modelss(self, list_id):
        try:
            Modelss.update(discount=0, sale=False, sale_price=0, sale_date_end=datetime.now()).\
                where(Modelss.id.in_(list_id)).execute()
        except DataError:
            pass

    def check_sales_products(self, list_id):
        try:
            Products.update(discount=0, sale=False, sale_price=0, sale_date_end=datetime.now()).\
                where(Products.modelss_id.in_(list_id)).execute()
        except DataError:
            pass

if __name__ == '__main__':

    data_check = CheckSales()
    data_check.get_sales()