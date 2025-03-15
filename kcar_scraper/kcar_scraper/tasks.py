from celery import shared_task
import os
import subprocess
import logging


@shared_task
def run_spiders_task():
    scrapy_project_path = '/kcar_scraper'

    spiders = ['kcar', 'mpark', 'charancha', 'bobaedream']

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
    translate_and_save("RuColorCar", "color", "ru_color", target_language='ru')


def clear_database(auction_value):
    from cars.models import AucCars

    AucCars.objects.filter(auction=auction_value).delete()
