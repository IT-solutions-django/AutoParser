import scrapy
import json
from urllib.parse import urlencode
from kcar_scraper.kcar_scraper.items import KcarScraperItem


class MparkSpider(scrapy.Spider):
    name = "mpark"
    start_urls = ["https://api.m-park.co.kr/home/api/v1/wb/searchmycar/carlistinfo/get?"]

    def start_requests(self):
        from cars.models import AucCars

        AucCars.objects.filter(auction="mpark").delete()

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
        car = response.meta["car"]
        details = json.loads(response.text).get("data", {}).get("detailInfo", {})[0]

        car_name = car['carName'].split(' ')[0]

        month_full = details.get('startYearMonth', '')
        if month_full:
            month = month_full.split('/')[1]
        else:
            month = None

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
            auction="mpark"
        )
