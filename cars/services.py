from .models import *
import logging 
from .sub_fun import calc_toll

logger = logging.getLogger(__name__)


def update_prices():
    cars_models = [AucCarsKorea, AucCarsJapan, AucCarsChina, AucCarsEurope, AucCarsRest]
    try:
        logging.info('Обновили валюты!')

        cars = AucCarsRest.objects.all()
        for car in cars:
            car.toll = int(calc_toll(car.finish, car.year, car.engine_volume, car.auc_table)[0])
            car.save()

        logging.info('Обновили авто')
    except Exception as e:
        print(f'Что-то не так с валютами !!!\n{e}')