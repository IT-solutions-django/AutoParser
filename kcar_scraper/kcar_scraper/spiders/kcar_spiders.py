import scrapy
import json
from urllib.parse import urlencode
from kcar_scraper.items import KcarScraperItem
from asgiref.sync import sync_to_async
from twisted.internet.threads import deferToThread


class KCarSpider(scrapy.Spider):
    name = "kcar"
    start_urls = ["https://api.kcar.com/bc/timeDealCar/list"]
    page = 1
    auction_value = "kcar"

    def start_requests(self):
        url = self.build_url(self.page)
        yield scrapy.Request(url, callback=self.parse, cookies=self.get_cookies())

    def build_url(self, page):
        params = {
            "currentPage": page,
            "pageSize": 18,
            "sIndex": 1,
            "eIndex": 10,
            "creatYn": "N",
        }
        return f"https://api.kcar.com/bc/timeDealCar/list?{urlencode(params)}"

    def get_cookies(self):
        return {
            'ab.storage.deviceId.79570721-e48c-4ca4-b9d6-e036e9bfeff8': '%7B%22g%22%3A%22b7404a2c-510b-12a8-560e-95604a58f89a%22%2C%22c%22%3A1732187811554%2C%22l%22%3A1732187811554%7D',
            'ab.storage.sessionId.79570721-e48c-4ca4-b9d6-e036e9bfeff8': '%7B%22g%22%3A%220eb30e25-7578-9663-a8fb-77a6be7f7ac7%22%2C%22e%22%3A1732190300903%2C%22c%22%3A1732187811597%2C%22l%22%3A1732188500903%7D',
        }

    def parse(self, response):
        data = json.loads(response.text)
        car_list = data.get("data", {}).get("list", [])

        if not car_list:
            return

        for car in car_list:
            car_id = car.get("carCd")
            details_url = f"https://api.kcar.com/bc/car-info-detail-of-ng?i_sCarCd={car_id}&i_sPassYn=N&bltbdKnd=CM050"

            yield scrapy.Request(details_url, callback=self.parse_details, meta={"car": car})

        self.page += 1
        yield scrapy.Request(self.build_url(self.page), callback=self.parse, cookies=self.get_cookies())

    def parse_details(self, response):
        car = response.meta["car"]
        details = json.loads(response.text).get("data", {}).get("rvo", {})
        photos = [p["elanPath"] for p in json.loads(response.text).get("data", {}).get("photoList", [])]

        yield KcarScraperItem(
            api_id=car.get("carCd"),
            brand=car.get("mnuftrNm"),
            model=car.get("modelNm"),
            year=car.get("prdcnYr"),
            mileage=car.get("milg"),
            color=car.get("extrColorNm"),
            finish=car.get("prc"),
            engine=car.get("fuelNm"),
            grade=car.get("grdNm"),
            equip=car.get("grdDtlNm"),
            drive=details.get("drvgYnNm"),
            engine_volume=details.get("engdispmnt"),
            transmission=details.get("trnsmsncdNm"),
            body_type=details.get("carctgr"),
            photos=photos,
            rate=None,
            month=None,
            power_volume=None,
            body_brand=None,
            lot=None,
            toll=None,
            auction="kcar"
        )
