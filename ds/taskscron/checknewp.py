from datetime import datetime
from taskscron.models import Modelss


def check_new():
    try:
        Modelss.update(is_new_date_end=datetime.now()).where(Modelss.is_new_date_end <= datetime.now()).execute()
    except EOFError:
        pass

check_new()