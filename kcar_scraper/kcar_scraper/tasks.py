from celery import shared_task
import os
import subprocess
import logging
from django.db import transaction


@shared_task
def run_spiders_task():
    scrapy_project_path = '/kcar_scraper'

    spiders = ['kcar', 'mpark', 'charancha']

    for spider in spiders:
        command = f"scrapy crawl {spider}"
        try:
            clear_database(spider)

            subprocess.run(command, shell=True, check=True, cwd=scrapy_project_path)

            post_process()

        except subprocess.CalledProcessError as e:
            logging.error(f"Ошибка при запуске {spider}: {e}")


def post_process():
    from cars.services import translate_and_save

    translate_and_save("RuBrandCar", "brand", "ru_brand")
    translate_and_save("RuModelCar", "model", "ru_model")


def clear_database(auction_value):
    from cars.models import AucCars

    AucCars.objects.filter(auction=auction_value).delete()


# def convert_in_toll(auction_value):
#     from cars.sub_fun import calc_toll
#     from cars.models import AucCars
#
#     BATCH_SIZE = 500
#
#     cars_auction = AucCars.objects.filter(auction=auction_value).only('id', 'finish', 'year', 'engine_volume', 'engine')
#     updated_cars = []
#
#     for car in cars_auction:
#         try:
#             if car.finish and car.finish != 'Не определено' and car.year and car.year != 0 and car.engine_volume and car.engine_volume != 'Не определено':
#                 engine = car.engine
#                 if engine in ['LPG+가솔린', '디젤+전기', '수소', '가솔린+전기', 'LPG+전기', 'LPG', '가솔린+LPG', '수소+전기', '기타', '가솔린/LPG겸용',
#                               '가솔린 하이브리드', '디젤 하이브리드']:
#                     engine_type = 3
#                 elif engine in ['전기']:
#                     engine_type = 2
#                 else:
#                     engine_type = None
#
#                 toll = calc_toll(int(car.finish) * 1000, int(car.year), int(car.engine_volume), 'korea', engine_type)
#
#                 car.toll = toll
#                 updated_cars.append(car)
#
#             if len(updated_cars) >= BATCH_SIZE:
#                 with transaction.atomic():
#                     AucCars.objects.bulk_update(updated_cars, ['toll'])
#                 updated_cars.clear()
#
#         except Exception as e:
#             print('Ошибка в пошлине на сайте аукциона. ', e)
#             continue
#
#     if updated_cars:
#         with transaction.atomic():
#             AucCars.objects.bulk_update(updated_cars, ['toll'])


