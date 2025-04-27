import requests
from .models import *
import logging
import time
from random import randint
from cars.sub_fun_2 import calc_price, get_akz


def fetch_card_car(api_id, drive, rate, photo, user_ip=None):
    try:
        url = f'http://31.130.151.223/api/get-auc-tables-data/korea/{api_id}'

        params = {
            'ip': user_ip
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            car = response.json().get('car', {})
            if car:
                country = CountryModels.objects.filter(brand=car.get('brand', '')).first()

                if car.get('engine', '') and car.get('engine', '') in ['Электро']:
                    if car.get('finish', '') not in [0, '0'] and car.get('year', 0) and car.get('year', 0) != 0 and car.get('engine_volume', '') and car.get('engine_volume', '') not in [0, '0']:
                        detailed_calculation = calc_price(int(car.get('finish', '')), int(car.get('year', 0)), int(car.get('engine_volume', '')), 'korea', 2)

                        akz = get_akz(1, int(car.get('year', 0)))
                        nds = (detailed_calculation["car_price_rus"] + detailed_calculation["toll"] + akz) * 0.2

                        detailed_calculation["total"] = detailed_calculation["total"] + akz + nds

                        toll = detailed_calculation["total"]

                    else:
                        toll = 0

                elif car.get('engine', '') and car.get('engine', '') in ['Гибрид']:
                    if car.get('finish', '') not in [0, '0'] and car.get('year', 0) and car.get('year', 0) != 0 and car.get('engine_volume', '') and car.get('engine_volume', '') not in [0, '0']:
                        detailed_calculation = calc_price(int(car.get('finish', '')), int(car.get('year', 0)), int(car.get('engine_volume', '')), 'korea', 3)

                        toll = detailed_calculation["total"]
                    else:
                        toll = 0

                elif car.get('engine', ''):
                    if car.get('finish', '') not in [0, '0'] and car.get('year', 0) and car.get('year', 0) != 0 and car.get('engine_volume', '') and car.get('engine_volume', '') not in [0, '0']:
                        detailed_calculation = calc_price(int(car.get('finish', '')), int(car.get('year', 0)),
                                                          int(car.get('engine_volume', '')), 'korea')

                        toll = detailed_calculation["total"]
                    else:
                        toll = 0

                else:
                    toll = 0

                car_obj, created = AucCars.objects.update_or_create(
                    api_id=api_id,
                    defaults={
                        'brand': car.get('brand', ''),
                        'lot': car.get('lot', ''),
                        'model': car.get('model', ''),
                        'year': car.get('year', 0),
                        'mileage': car.get('mileage', 0),
                        'toll': toll,
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

                if photo:
                    photo_obj, _ = AucCarsPhoto.objects.get_or_create(url=photo)
                    car_obj.photos.clear()
                    car_obj.photos.add(photo_obj)
        else:
            logging.error(f'Ошибка при запросе к карточке авто. Статус ответа: {response.status_code}')
    except Exception as e:
        logging.error(f'Не удалось сохранить авто. Ошибка: {e}')


def fetch_catalog_car(user_ip=None, country=None):
    page = 1

    while True:
        try:
            params = {
                'page': page
            }
            url = f'http://31.130.151.223/api/get-auc-tables-data/{country}/'

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
                        photo = car.get('first_photo_url', '')

                        fetch_card_car(api_id, drive, rate, photo, user_ip=user_ip)

                    page += 1

                    time.sleep(randint(30, 50))
            else:
                logging.error(f'Ошибка при запросе к каталогу. Статус ответа: {response.status_code}')
                break
        except Exception as e:
            logging.error(f'Не удалось спарсить страницу {page} с каталогом. Ошибка: {e}')
            break
