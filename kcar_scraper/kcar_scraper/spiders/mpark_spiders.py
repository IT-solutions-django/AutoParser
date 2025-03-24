import scrapy
import json
from urllib.parse import urlencode
from kcar_scraper.items import KcarScraperItem
from asgiref.sync import sync_to_async


class MparkSpider(scrapy.Spider):
    name = "mpark"
    start_urls = ["https://api.m-park.co.kr/home/api/v1/wb/searchmycar/carlistinfo/get?"]
    auction_value = "mpark"

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], callback=self.parse, cookies=self.get_cookies())

    def get_cookies(self):
        return {}

    def parse(self, response):
        data = json.loads(response.text)
        car_list = data.get("data", [])

        if not car_list:
            return

        for car in car_list:
            car_id = car.get("demoNo")
            details_url = f"https://api.m-park.co.kr/home/api/v1/wb/searchmycar/cardetailinfo/get?demoNo={car_id}"

            yield scrapy.Request(details_url, callback=self.parse_details, meta={"car": car})

    def parse_details(self, response):
        from cars.sub_fun import calc_toll

        car = response.meta["car"]
        details = json.loads(response.text).get("data", {}).get("detailInfo", {})[0]

        car_name = car['carName'].split(' ')[0]

        month_full = details.get('startYearMonth', '')
        if month_full:
            month = month_full.split('/')[1]
        else:
            month = None

        toll = None

        try:
            if car.get('demoAmt') and car.get('yyyy') and details.get("numCc"):

                if details.get("carGas") in ['LPG+가솔린', '디젤+전기', '수소', '가솔린+전기', 'LPG+전기', 'LPG', '가솔린+LPG', '수소+전기', '기타',
                                         '가솔린/LPG겸용', '가솔린 하이브리드', '디젤 하이브리드']:
                    engine_type = 3
                elif details.get("carGas") in ['전기']:
                    engine_type = 2
                else:
                    engine_type = None

                toll = calc_toll(int(car.get('demoAmt')), int(car.get('yyyy')), int(details.get("numCc")), 'korea',
                                 engine_type)
        except Exception as e:
            print('Ошибка в пошлине на сайте аукциона. ', e)

        yield KcarScraperItem(
            api_id=car.get("demoNo"),
            brand=car_name,
            model=details.get("modelDetailName"),
            year=car.get("yyyy"),
            mileage=details.get("km"),
            color=details.get("carColor"),
            finish=car.get("demoAmt"),
            engine=details.get("carGas"),
            grade=None,
            equip=None,
            drive=None,
            engine_volume=details.get("numCc"),
            transmission=details.get("carAutoGbn"),
            body_type=details.get("carType"),
            photos=details["images"],
            rate=None,
            month=month,
            power_volume=None,
            body_brand=None,
            lot=None,
            toll=toll,
            auction="mpark"
        )
