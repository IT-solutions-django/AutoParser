import scrapy
import json
from urllib.parse import urlencode
from kcar_scraper.items import KcarScraperItem
import xml.etree.ElementTree as ET
from asgiref.sync import sync_to_async


class CharanchaSpider(scrapy.Spider):
    name = "charancha"
    start_urls = ["https://charancha.com/v1/cars"]
    page = 1
    auction_value = "charancha"

    def start_requests(self):
        url = self.build_url(self.page)
        yield scrapy.Request(url, callback=self.parse, cookies=self.get_cookies())

    def build_url(self, page):
        params = {
            'page': page,
            'size': 150
        }
        return f"https://charancha.com/v1/cars?{urlencode(params)}"

    def get_cookies(self):
        return {}

    def parse(self, response):
        from cars.sub_fun import calc_toll

        root = ET.fromstring(response.text)
        car_list = root.findall(".//content")

        if not car_list:
            return

        for car in car_list:
            finish_toll = car.find("sellPrice").text if car.find("sellPrice") is not None else None
            year_toll = car.find("modelYyyyDt").text if car.find("modelYyyyDt") is not None else None
            engine_volume_toll = car.find("displacement").text if car.find("displacement") is not None else None
            engine_toll = car.find("fuelNm").text if car.find("fuelNm") is not None else None

            toll = None

            try:
                if finish_toll and year_toll and engine_volume_toll:

                    if engine_toll in ['LPG+가솔린', '디젤+전기', '수소', '가솔린+전기', 'LPG+전기', 'LPG', '가솔린+LPG',
                                                 '수소+전기', '기타',
                                                 '가솔린/LPG겸용', '가솔린 하이브리드', '디젤 하이브리드']:
                        engine_type = 3
                    elif engine_toll in ['전기']:
                        engine_type = 2
                    else:
                        engine_type = None

                    toll = calc_toll(int(finish_toll), int(year_toll), int(engine_volume_toll), 'korea',
                                     engine_type)
            except Exception as e:
                print('Ошибка в пошлине на сайте аукциона. ', e)

            yield KcarScraperItem(
                api_id=car.find("sellNo").text if car.find("sellNo") is not None else None,
                brand=car.find("makerNm").text if car.find("makerNm") is not None else None,
                model=car.find("modelNm").text if car.find("modelNm") is not None else None,
                year=car.find("modelYyyyDt").text if car.find("modelYyyyDt") is not None else None,
                mileage=car.find("mileage").text if car.find("mileage") is not None else None,
                color=car.find("colorNm").text if car.find("colorNm") is not None else None,
                finish=car.find("sellPrice").text if car.find("sellPrice") is not None else None,
                engine=car.find("fuelNm").text if car.find("fuelNm") is not None else None,
                grade=car.find("gradeNm").text if car.find("gradeNm") is not None else None,
                equip=car.find("gradeDetailNm").text if car.find("gradeDetailNm") is not None else None,
                drive=None,
                engine_volume=car.find("displacement").text if car.find("displacement") is not None else None,
                transmission=car.find("transmissionNm").text if car.find("transmissionNm") is not None else None,
                body_type=car.find("bodyTypeNm").text if car.find("bodyTypeNm") is not None else None,
                photos=[car.find("carImg").text] if car.find("carImg") is not None else [],
                rate=None,
                month=None,
                power_volume=None,
                body_brand=None,
                lot=None,
                toll=toll,
                auction="charancha"
            )

        self.page += 1
        yield scrapy.Request(self.build_url(self.page), callback=self.parse, cookies=self.get_cookies())
