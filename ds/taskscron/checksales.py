from peewee import *
from datetime import datetime
from taskscron.models import Modelss, Products


class CheckSales:

    def check_sales(self):
        self.check_sales_modelss()
        self.check_sales_products()

    def check_sales_modelss(self):
        try:
            Modelss.update(is_new_date_end=datetime.now(), is_new=False).\
                where(Modelss.is_new_date_end <= datetime.now()).execute()
        except DataError:
            pass

    def check_sales_products(self):
        try:
            Products.update(is_new_date_end=datetime.now(), is_new=False).\
                where(Products.is_new_date_end <= datetime.now()).execute()
        except DataError:
            pass

if __name__ == '__main__':

    data_check = CheckSales()
    data_check.check_sales()