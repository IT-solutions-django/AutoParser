import scrapy
import re
import json
from urllib.parse import urlencode
from kcar_scraper.items import KcarScraperItem


class MdcarSpider(scrapy.Spider):
    name = "mdcar"
    start_urls = ["http://mdcar.kr/search/list_ajax.mdc"]
    page = 1

    def start_requests(self):
        url = self.build_url(self.page)
        yield scrapy.Request(url, callback=self.parse, cookies=self.get_cookies())

    def build_url(self, page):
        params = {
            "mode": "list",
            "ct": -2,
            "pg": page,
            "cnt": 16,
            "jsoncallback": "jQuery171035174765392992535_1741226547997"
        }
        return f"http://mdcar.kr/search/list_ajax.mdc?{urlencode(params)}"

    def get_cookies(self):
        return {}

    def parse(self, response):
        match = re.search(r'\((.*)\)', response.text)

        if not match:
            return

        json_data = match.group(1)

        json_data = re.sub(r'([a-zA-Z0-9_]+):', r'"\1":', json_data)

        data = json.loads(json_data)
        car_list = data.get("data", [])

        if not car_list:
            return

        for car in car_list:
            car_id = car.get("i")
            details_url = f"http://mdcar.kr/usedcar/detail_ajax.mdc?mode=detail&id={car_id}&jsoncallback=jQuery171006607303846524393_1741227787854"

            yield scrapy.Request(details_url, callback=self.parse_details, meta={"car": car})

        self.page += 1
        yield scrapy.Request(self.build_url(self.page), callback=self.parse, cookies=self.get_cookies())

    def parse_details(self, response):
        car = response.meta["car"]
        match = re.search(r'\((.*)\)', response.text)

        if not match:
            return

        json_data = match.group(1)

        json_data = re.sub(r'([a-zA-Z0-9_]+):', r'"\1":', json_data)

        details = json.loads(json_data)

        month_full = details.get("regYear")
        if month_full:
            month = month_full.split('-')[1]
        else:
            month = None

        yield KcarScraperItem(
            api_id=car.get("i"),
            brand=car.get("bn"),
            model=car.get("mn"),
            year=car.get("y"),
            mileage=car.get("mi"),
            color=details.get("color"),
            finish=car.get("p"),
            engine=details.get("fuel"),
            grade=car.get("cn"),
            equip=None,
            drive=None,
            engine_volume=details.get("disp"),
            transmission=car.get("t"),
            body_type=None,
            photos=[],
            rate=None,
            month=month,
            power_volume=None,
            body_brand=None,
            lot=None,
            auction="mdcar"
        )
