import requests
from .models import *
import logging
import time
from random import randint


def fetch_card_car(api_id, drive, rate):
    try:
        url = f'http://31.130.151.223/api/get-auc-tables-data/korea/{api_id}/'

        params = {
            'ip': '193.164.149.51'
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            car = response.json().get('car', {})
            if car:
                country = CountryModels.objects.filter(brand=car.get('brand', '')).first()

                car_obj, created = AucCars.objects.update_or_create(
                    api_id=api_id,
                    defaults={
                        'brand': car.get('brand', ''),
                        'lot': car.get('lot', ''),
                        'model': car.get('model', ''),
                        'year': car.get('year', 0),
                        'mileage': car.get('mileage', 0),
                        'toll': car.get('price', 0),
                        'transmission': car.get('transmission', ''),
                        'engine_volume': car.get('engine_volume', ''),
                        'drive': drive,
                        'color': car.get('color', ''),
                        'rate': rate,
                        'finish': car.get('finish', ''),
                        'engine': car.get('engine', ''),
                        'is_active': True,
                        'auction': 'encar',
                        'brand_country': country
                    }
                )
        else:
            logging.error(f'Ошибка при запросе к карточке авто. Статус ответа: {response.status_code}')
    except Exception as e:
        logging.error(f'Не удалось сохранить авто. Ошибка: {e}')


def fetch_catalog_car():
    page = 1

    while True:
        try:
            params = {
                'page': page
            }
            url = 'http://31.130.151.223/api/get-auc-tables-data/korea/'

            response = requests.get(url, params=params)

            if response.status_code == 200:
                cars = response.json().get('cars', [])
                if not cars:
                    break
                else:
                    for car in cars:
                        api_id = car.get('api_id', '')
                        drive = car.get('drive', '')
                        rate = car.get('rate', '')

                        fetch_card_car(api_id, drive, rate)

                    page += 1

                    time.sleep(randint(30, 50))
            else:
                logging.error(f'Ошибка при запросе к каталогу. Статус ответа: {response.status_code}')
                break
        except Exception as e:
            logging.error(f'Не удалось спарсить страницу {page} с каталогом. Ошибка: {e}')
            break
