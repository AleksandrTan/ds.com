from datetime import datetime
from taskscron.models import Modelss, Products


def check_new():
    try:
        Modelss.update(is_new_date_end=datetime.now(), is_new=False).\
            where(Modelss.is_new_date_end <= datetime.now()).execute()

        Products.update(is_new_date_end=datetime.now(), is_new=False).\
            where(Products.is_new_date_end <= datetime.now()).execute()
    except EOFError:
        pass

if __name__ == '__main__':
    check_new()