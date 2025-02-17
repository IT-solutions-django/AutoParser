from bs4 import BeautifulSoup
from typing import Iterable
import requests
from datetime import datetime, timedelta
from .models import *
from .models import Color
from random import randint
import time
import logging
import re

# Настройка логирования
logging.basicConfig(
    filename='errors.log',       
    level=logging.ERROR,           
    format='%(asctime)s - %(levelname)s - %(message)s' 
)


def get_client_ip():
    return f'192.168.{randint(0, 255)}.{randint(0, 255)}'


def get_user_ip(request):
    # Получаем User-Agent
    user_agent = request.META.get('HTTP_USER_AGENT', '')

    # Проверяем, является ли это Googlebot
    if 'Googlebot' in user_agent or 'YandexBot' in user_agent:
        ip =f'141.{randint(0, 255)}.{randint(0, 255)}.33'
    else:
        # Получаем IP-адрес
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
    
    return ip


def get_sql_query(
    fields: str,
    table_name: str,
    base_filters: Iterable[str],
    limit: str,
):
    filter_statements = list(base_filters.values())
    
    query = f"select+{fields}+from+{table_name}+WHERE+1+=+1+and+{'+and+'.join(map(str, filter_statements))}+limit+{limit}"

    return query


def get_simple_sql_query(
    fields: str,
    table_name: str,
    limit: str,
):    
    query = f"select+{fields}+from+{table_name}+WHERE+1+=+1+limit+{limit}"

    return query


def fetch_by_query(sql_query, user_ip=None):
    user_ip = user_ip if user_ip else get_client_ip()
    try:
        url = f"http://78.46.90.228/api/?ip={user_ip}&code=TDAjhTr53Sd9&sql={sql_query}"
        print(url)
        res = requests.get(url)
        soup = BeautifulSoup(res.content.decode("utf-8"), "xml")
        return [
            {elem.name: elem.getText() for elem in row.findChildren()}
            for row in soup.findAll("row")
        ]
    except Exception as e:
        print('Повторный запрос')
        print(str(e))
        fetch_by_query(sql_query, user_ip)


def get_base_filters(table_name: str):
    base_filers = Filterss.objects.get(table_filter__name=table_name)
    auctions = "','".join([str(m) for m in base_filers.auction.all()])
    marks = "','".join([str(m) for m in base_filers.marka_name.all()])
    result = {
        "AUCTION": f"AUCTION+NOT+IN+('{auctions}')",
        "MARKA_NAME": f"MARKA_NAME+NOT+IN+('{marks}')",
        "YEAR": f"YEAR+>=+{base_filers.year_filter}",
        "ENG_V_to": f"ENG_V+<=+{base_filers.eng_filter_max}",
        "ENG_V_from": f"ENG_V+>=+{base_filers.eng_filter_min}",
        "MILEAGE": f"MILEAGE+<=+{base_filers.mileage_filter}",
        "FINISH": f"FINISH+>+{base_filers.finish}",
        "STATUS": "STATUS+NOT+IN+('Not+sold')",
    }

    if (table_name == 'stats'):
        min_auction_date = (datetime.today().date() - timedelta(days=int(7)))
        max_auction_date = datetime.today().date()

        result.update(
            {
                "AUCTION_DATE": f"AUCTION_DATE+<=+'{max_auction_date}'+and+AUCTION_DATE+>=+'{min_auction_date}'",
                "STATUS": "STATUS+LIKE+'%Sold%'+and+STATUS+!=+'Not+Sold'",
            }
        )
    else:
         result.update(
            {
                 "STATUS": "STATUS+NOT+IN+('Not+sold')",
            }
        )

    if base_filers.rate.exists():
        result.update(
            {
                "RATE": f"RATE IN ('{','.join([str(m) for m in base_filers.rate.all()])}')",
            }
        )
    return result


def get_car_api_photos_by_id(car_id: str, user_ip: str, table_name: str):
    query = f"select+*+from+{table_name}+WHERE+1+=+1+and+id+=+'{car_id}'"

    data = fetch_by_query(query, user_ip)

    if(data):
        car = data[0]
    else:
        return False
    

    photos = [image for image in car["IMAGES"].split("#")]
    if(table_name == 'stats'):
       photos = [photos[1], photos[2], photos[0], *photos[3:]]
    
    return photos

def get_cars_count(table_name: str, filters: list[str]):
    query = get_sql_query(
        "count(*)",
        table_name,
        filters,
        "0,1",
    )
    data = fetch_by_query(query)
    return data[0]["TAG0"]


def save_to_db(table, car, model, brand_country):
    try:
        print('пробуем')
        if table == 'stats':
            active = True
        else:
            print('неактивный')
            active = False

        color_tag = Color.objects.filter(api_value=car["COLOR"]).first()
        engine = car["TIME"]

        print(engine)

        if(engine == 'D'):
            engine_type_name = 'Дизель'
        elif(engine in ('G', 'C', 'L', 'P')):
            engine_type_name = 'Бензин'
        else:
            engine_type_name = 'Бензин'
            
        if(engine == 'E'):
            engine_type = 2
            engine_type_name = 'Электро'
        elif(engine == 'H'):
            engine_type = 3
            engine_type_name = 'Гибрид'
        else:
            engine_type = None

        print(engine)
        # print(model)
        
        car_obj, created = model.objects.get_or_create(
                auc_table = table,
                auc_name = car["AUCTION"],    
                auc_date = car["AUCTION_DATE"],    
                api_id = car["ID"],
                brand = car["MARKA_NAME"],
                model = car["MODEL_NAME"],
                brand_country=brand_country,
                year = int(car["YEAR"]),
                kuzov = car["KUZOV"],
                mileage = int(car["MILEAGE"]),
                # price = int(
                #     calc_price(
                #         car["FINISH"], car["YEAR"], car["ENG_V"], table, engine_type
                #     )[0]
                # ),
                transmission="Механика" if car["KPP_TYPE"] == '1' else "Автомат",
                engine_volume = car["ENG_V"],
                drive=(
                    "Передний привод" if car["PRIV"] == "FF" else
                    "Задний привод" if car["PRIV"] in ("FR", "MR", "RR") else
                    "Полный привод"
                ),
                color=color_tag.value.true_value if color_tag is not None else car["COLOR"],
                rate = car["RATE"],
                finish = car["FINISH"],
                power_volume = int(car["PW"]) if car.get("PW") else 0,
                is_active = active,
                lot=car["LOT"],
                rubber='Правый руль' if table == 'stats' else 'Левый руль',
                engine = engine_type_name,
        )
        print(f'Объект машины: {car_obj}')

        if created:
            photo_urls = car["IMAGES"].split('#')

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
        print(e)


    

def check_model_manifacture(brand, id):
    try:
        print(brand)
        if 'BAIC' in brand:
            brand_country = CountryModels.objects.get(brand='BAIC')
        else:
            brand_country =  CountryModels.objects.get(brand=brand)
                
        # Определяем модель в зависимости от страны бренда
        if brand_country.country == 'Япония':
            return AucCarsJapan, brand_country
        elif brand_country.country == 'Корея':
            return AucCarsKorea, brand_country
        elif brand_country.country == 'Китай':
            return AucCarsChina, brand_country
        elif brand_country.country == 'Европа':
            return AucCarsEurope, brand_country
        elif brand_country.country == 'США':
            return AucCarsUSA, brand_country
    except Exception as e:
            logging.error(f"Нет макри !!!!!!! {brand}, ID авто - {id}: {e}")

            brand_country = CountryModels.objects.create(country="Корея", brand=brand)
            brand_country.save()


            return AucCars, brand_country
            
cars_models = [AucCarsKorea, AucCarsJapan, AucCarsChina, AucCarsEurope]
def delete_dublicate():
    for model_c in cars_models:
        cars = model_c.objects.all()
        try:
            for car in cars:
                duplicates = model_c.objects.filter(api_id=car.api_id).exclude(id=car.id)
                print(car.api_id)
                if duplicates.exists():
                    print(f"Удаляем дубликаты для api_id: {car.api_id}")
                    duplicates.delete()

        except Exception as e:
            print(e)

def change_colors():
    color_pattern = r"'([^']+)'"
    for model_c in [AucCarsEurope, ]:
        cars = model_c.objects.all()
        try:
            for car in cars:
                color_tag = Color.objects.filter(api_value__icontains=car.color).first()
                print(color_tag)
                if color_tag:
                    car.color=color_tag.value.true_value
                    car.save()
        except Exception as e:
            print(e)

def change_rubber():
    for model_c in cars_models:
        cars = model_c.objects.all()
        try:
            for car in cars:
                
                if(car.auc_table != 'stats'):
                    car.rubber = 'Левый руль'
                else:
                    car.rubber = 'Правый руль'
                car.save()
                print(car.rubber)

        except Exception as e:
            print(e)



def parse_japan():
    # отчистка невалидных данных
    table = 'stats'
    for model_c in cars_models:
        last_date = (datetime.today().date() - timedelta(days=int(31)))
        cars = model_c.objects.filter(auc_date__lt=last_date, auc_table=table).order_by('auc_date')
        for car in cars:
            car.delete()
        
    
    # filters = get_base_filters(table)
    # cars_count = get_cars_count(table, filters)
    cars_count = 1000
    pages = int(cars_count) / 250
    page = 0
    try:
        while (page <= pages):
            query = get_simple_sql_query(
                "*", 
                table, 
                f"250,1",
            )
            # query = get_sql_query(
            #     "*",
            #     table,
            #     filters,
            #     f"{250 * page},{(250 * page) + 250 }",
            # )
            data = fetch_by_query(query)

            print(data)

            for car in data:
                try:
                    print(car)
                    model, country = check_model_manifacture(car["MARKA_NAME"], car["ID"])
                    save_to_db(table, car, AucCars, country)
                except Exception as e:
                    logging.error(f"Ошибка при обработке автомобиля с ID {car['ID']}: {e}")
                    continue  

            page += 1

            print(f'Страница {page}')

            time.sleep(randint(20, 30)) 
    except Exception as e:
        logging.error(f"Ошибка Япония: {e}")
        return None

def parse_china():
    table = 'china'
    for model_c in cars_models:
            objects = model_c.objects.filter(auc_table=table)
            for car in objects:
                car.is_active = False
                car.save()
    
    filters = get_base_filters(table)
    cars_count = get_cars_count(table, filters)
    pages = int(cars_count) / 250
    page = 0
    try:
        while (page <= pages):
            query = get_sql_query(
                "*",
                table,
                filters,
                f"{250 * page},{(250 * page) + 250 }",
            )
            data = fetch_by_query(query)

            for car in data:
                try:
                    result = check_model_manifacture(car["MARKA_NAME"], car["ID"])
                    car["AUCTION_DATE"] = datetime.now()
                    model, country = result
                    save_to_db(table, car, model,country)
                except Exception as e:
                    logging.error(f"Ошибка при обработке автомобиля с ID {car['ID']}: {e}")
                    continue  
            page += 1
            

            delay = randint(20, 30)
            logging.info(f"Задержка: {delay} секунд между запросами.")
            time.sleep(delay)
        
        for model_c in cars_models:
            objects = model_c.objects.filter(auc_table=table, is_active=False)
            for car in objects:
                car.delete()
    except Exception as e:
            logging.error(f"Ошибка Китай: {e}")
            return None

def parse_korea():
    table = 'korea'
    for model_c in cars_models:
            objects = model_c.objects.filter(auc_table=table)
            for car in objects:
                car.is_active = False
                car.save()

    cars_count = 1000
    pages = int(cars_count) / 250
    page = 0
    try:
        while (page <= pages):
            query = get_simple_sql_query(
                "*", 
                table, 
                f"{250 * page},{(250 * page) + 250 }",
            )
            data = fetch_by_query(query)

            for car in data:
                try:
                    print(car)
                    result = check_model_manifacture(car["MARKA_NAME"], car["ID"])
                    print(f'result = {result}')
                    car["AUCTION_DATE"] = datetime.now()


                    model, country = result


                    save_to_db(table, car, AucCars ,country)
                except Exception as e:
                    print(str(e))
                    logging.error(f"Ошибка при обработке автомобиля с ID {car['ID']}: {e}")
                    continue  
            page += 1
            

            time.sleep(randint(20, 30))

        for model_c in cars_models:
            objects = model_c.objects.filter(auc_table=table, is_active=False)
            for car in objects:
                car.delete() 
    except Exception as e:
            logging.error(f"Ошибка Корея: {e}")
            return None



def revrite_color():
    cars = AucCarsEurope.objects.all()
    for car in cars:
        color = car.color
        color_tag = Color.objects.filter(api_value=color).first()
        car.color=color_tag.true_value if color_tag is not None else color
        car.save()
       
def change_engine_type():
    for model_c in cars_models:
        objects = model_c.objects.filter(engine__isnull=True)
        for car in objects:
            query = f"select+*+from+{car.auc_table}+WHERE+1+=+1+and+id+=+'{car.api_id}'"

            data = fetch_by_query(query)
            print(data)
            if(data):
                car_api = data[0]
                if(car_api['TIME'] == 'D'):
                    engine_type_name = 'Дизель'
                elif(car_api['TIME'] == 'E'):
                    engine_type = 2
                    engine_type_name = 'Электро'
                elif(car_api['TIME'] == 'H'):
                    engine_type = 3
                    engine_type_name = 'Гибрид'
                elif(car_api['TIME'] in ('G', 'C', 'L', 'P')):
                    engine_type_name = 'Бензин'
                else:
                    engine_type_name = 'Бензин'
                car.engine = engine_type_name
                car.save()
            else:
                car.delete()
            time.sleep(randint(20, 30))


def clean_USA():
    AucCarsUSA.objects.all().delete()
