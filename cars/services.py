from .models import AucCars
import logging 
from .sub_fun import calc_price

logger = logging.getLogger(__name__)


def update_prices():
    try:
        logging.info('Обновили валюты!')

        cars = AucCars.objects.all()
        for car in cars:
            car.price = int(calc_price(car.finish, car.year, car.engine_volume, car.auc_table)[0])
            car.save()

        logging.info('Обновили авто')
    except Exception as e:
        print(f'Что-то не так с валютами !!!\n{e}')