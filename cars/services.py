from django.db import transaction

from .models import *
import logging
import requests
from .sub_fun import calc_toll
import json
from .config import SITE_URLS
from .auc_parser import check_model_manifacture
import time
from django.apps import apps

logger = logging.getLogger(__name__)


def save_to_db(car, auction) -> None:
    """Функция для сохранения авто в БД"""

    try:
        result = check_model_manifacture(car["brand"], car["api_id"])
        model, country = result

        car_obj, created = model.objects.get_or_create(
            auction=auction,
            api_id=car["api_id"],
            brand=(car["brand"] if car["brand"] else 'Не определено'),
            model=(car["model"] if car["model"] else 'Не определено'),
            brand_country=country,
            year=(car["year"] if car["year"] else 0),
            body_brand=car["body_brand"],
            mileage=(int(float(car["mileage"])) if car["mileage"] else 0),

            toll=350,  # FIXME: надо будет добавить полученное значение из calc_toll

            transmission=(car["transmission"] if car["transmission"] else 'Не определено'),
            engine_volume=(car["engine_volume"] if car["engine_volume"] else 'Не определено'),
            drive=(car["drive"] if car["drive"] else 'Не определено'),
            color=(car["color"] if car["color"] else 'Не определено'),
            rate=(car["rate"] if car["rate"] else 'Не определено'),
            finish=(car["finish"] if car["finish"] else 'Не определено'),
            power_volume=car["power_volume"],

            is_active=True,  # TODO: понять, за что отвечает данное поле

            lot=(car["lot"] if car["lot"] else 'Не определено'),

            engine=car["engine"],  # FIXME: надо будет добавить значение, которое соответствует dropdown в админке

            month=car["month"],
            grade=car["grade"],
            equip=car["equip"],
            body_type=car['body_type']
        )

        if created:
            photo_urls = car["photos"]

            if photo_urls:

                photo_objects = []
                for url in photo_urls:
                    photo, _ = AucCarsPhoto.objects.get_or_create(url=url)
                    photo_objects.append(photo)

                car_obj.photos.add(*photo_objects)

            car_obj.is_active = True
            car_obj.save()
        else:
            car_obj.is_active = True
            car_obj.save()
    except Exception as e:
        logger.error(f'Ошибка при сохранении авто {car.get("api_id")}: {e}')


def parse_card_kcar(settings, cookies, car_id) -> dict:
    """Функция для запроса к карточке авто сайта kcar"""

    url = f'https://api.kcar.com/bc/car-info-detail-of-ng?i_sCarCd={car_id}&i_sPassYn=N&bltbdKnd=CM050'

    try:
        response = requests.get(url, cookies=cookies)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Ошибка запроса к {url}: {e}")
        return {}

    photos_list = []

    photos = response.json()['data']['photoList']
    if photos:
        for photo in photos:
            photos_list.append(photo['elanPath'])

    data_car = response.json()['data']['rvo']
    new_param = {
        'drive': data_car.get('drvgYnNm'),
        'photos': photos_list,
        'engine_volume': data_car.get('engdispmnt'),
        'transmission': data_car.get('trnsmsncdNm'),
        'body_type': data_car.get('carctgr')
    }

    return new_param


def parse_kcar() -> None:
    """Функция для парсинга каталога авто сайта kcar"""

    kcar_setttings = SITE_URLS.KCar
    current_page = 1

    while True:
        params = {
            'currentPage': current_page,
            'pageSize': 18,
            'sIndex': 1,
            'eIndex': 10,
            'creatYn': 'N',
        }
        url = kcar_setttings.catalog_url
        cookies = kcar_setttings.cookies

        try:
            response = requests.get(url, params=params, cookies=cookies)
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"Ошибка запроса к {url}: {e}")
            return None

        data_cars = response.json()['data']['list']

        if data_cars:
            for data_car in data_cars:
                car = {
                    'api_id': data_car.get('carCd'),
                    'brand': data_car.get('mnuftrNm'),
                    'model': data_car.get('modelNm'),
                    'year': data_car.get('prdcnYr'),
                    'mileage': data_car.get('milg'),
                    'color': data_car.get('extrColorNm'),
                    'finish': data_car.get('prc'),
                    'engine': data_car.get('fuelNm'),
                    'grade': data_car.get('grdNm'),
                    'equip': data_car.get('grdDtlNm'),
                    'month': None,
                    'power_volume': None,
                    'rate': None,
                    'body_brand': None,
                    'lot': None
                }

                car_data_card = parse_card_kcar(kcar_setttings, cookies, data_car['carCd'])

                car['photos'] = car_data_card.get('photos')
                car['drive'] = car_data_card.get('drive')
                car['engine_volume'] = car_data_card.get('engine_volume')
                car['transmission'] = car_data_card.get('transmission')
                car['body_type'] = car_data_card.get('body_type')

                save_to_db(car, 'kcar')

                time.sleep(10)

            current_page += 1

        else:
            break


def parce_card_mpark(car_id) -> dict:
    """Функция для запроса к карточке авто сайта mpark"""

    url = f"https://api.m-park.co.kr/home/api/v1/wb/searchmycar/cardetailinfo/get?demoNo={car_id}"

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Ошибка запроса к {url}: {e}")
        return {}

    data_car = response.json()['data']['detailInfo'][0]

    month_full = data_car.get('startYearMonth', '')
    if month_full:
        month = month_full.split('/')[1]
    else:
        month = None

    new_param = {
        'model': data_car.get('modelDetailName'),
        'mileage': data_car.get('km'),
        'photos': data_car.get('images'),
        'body_type': data_car.get('carType'),
        'transmission': data_car.get('carAutoGbn'),
        'engine_volume': data_car.get('numCc'),
        'color': data_car.get('carColor'),
        'engine': data_car.get('carGas'),
        'month': month,
    }

    return new_param


def parse_mpark() -> None:
    """Функция для парсинга каталога авто сайта mpark"""

    mpark_setttings = SITE_URLS.Mpark

    url = mpark_setttings.catalog_url

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Ошибка запроса к {url}: {e}")
        return None

    data_cars = response.json()['data']

    if data_cars:
        for data_car in data_cars:
            car_name = data_car['carName'].split(' ')[0]
            car = {
                'api_id': data_car.get('demoNo'),
                'brand': car_name,
                'year': data_car.get('yyyy'),
                'finish': data_car.get('demoAmt'),
                'grade': None,
                'equip': None,
                'power_volume': None,
                'rate': None,
                'body_brand': None,
                'lot': None,
                'drive': None
            }

            car_data_card = parce_card_mpark(data_car['demoNo'])

            for key in car_data_card.keys():
                car[key] = car_data_card.get(key)

            save_to_db(car, 'mpark')

            time.sleep(10)


def parse_charancha() -> None:
    """Функция для парсинга каталога авто сайта charancha"""

    charancha_setttings = SITE_URLS.Charancha
    url = charancha_setttings.catalog_url

    current_page = 0

    while True:

        params = {
            'currentPage': current_page,
            'size': 150
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"Ошибка запроса к {url}: {e}")
            return None

        data_page = response.json()['page']
        total_page = data_page['totalPages']

        data_cars = response.json()['_embedded']['cars']

        if data_cars:
            for data_car in data_cars:
                car = {
                    'api_id': data_car.get('sellNo'),
                    'brand': data_car.get('makerNm'),
                    'model': data_car.get('modelNm'),
                    'year': data_car.get('modelYyyyDt'),
                    'mileage': data_car.get('mileage'),
                    'photos': [data_car.get('carImg')],
                    'finish': data_car.get('sellPrice'),
                    'body_type': data_car.get('bodyTypeNm'),
                    'transmission': data_car.get('transmissionNm'),
                    'engine_volume': data_car.get('displacement'),
                    'drive': None,
                    'color': data_car.get('colorNm'),
                    'engine': data_car.get('fuelNm'),
                    'grade': data_car.get('gradeNm'),
                    'equip': data_car.get('gradeDetailNm'),
                    'power_volume': None,
                    'rate': None,
                    'body_brand': None,
                    'lot': None,
                    'month': None
                }

                save_to_db(car, 'charancha')

        if current_page == total_page:
            break

        time.sleep(10)

        current_page += 1


API_KEY = "AQVN2HsU0I5W71AKDUpBpVPqxcBUEIfwBvSLT6Ua"
URL = "https://translate.api.cloud.yandex.net/translate/v2/translate"


def create_headers():
    return {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {API_KEY}"
    }


def translate_and_save(model_name, original_field, translated_field, target_language="en", source_language="ko"):

    ModelClass = apps.get_model("cars", model_name)

    existing_values = ModelClass.objects.values_list(original_field, flat=True)
    new_values = list(
        AucCars.objects.exclude(**{f"{original_field}__in": existing_values}).values_list(original_field, flat=True).distinct()
    )

    if not new_values:
        return

    batch_size = 100
    batches = [new_values[i:i + batch_size] for i in range(0, len(new_values), batch_size)]

    for batch in batches:
        data = {
            "targetLanguageCode": target_language,
            "texts": batch,
            "sourceLanguageCode": source_language
        }

        response = requests.post(URL, headers=create_headers(), json=data)

        if response.status_code == 200:
            translations = response.json().get("translations", [])

            translated_objects = [
                ModelClass(**{original_field: orig, translated_field: trans["text"]})
                for orig, trans in zip(batch, translations)
            ]

            with transaction.atomic():
                ModelClass.objects.bulk_create(translated_objects)

        else:
            logger.error("Ошибка:", response.status_code, response.text)
