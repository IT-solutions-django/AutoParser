import scrapy
import json
from urllib.parse import urlencode
from kcar_scraper.kcar_scraper.items import KcarScraperItem


class AutoInsideSpider(scrapy.Spider):
    name = "autoinside"
    start_urls = ["https://www.autoinside.co.kr/display/bu/display_bu_used_car_list_ajax.do"]
    page = 1
    max_pages = 24

    def start_requests(self):
        url = self.build_url(self.page)
        yield scrapy.Request(url, callback=self.parse, cookies=self.get_cookies())

    def build_url(self, page):
        params = {
            "i_iNowPageNo": page
        }
        return f"https://www.autoinside.co.kr/display/bu/display_bu_used_car_list_ajax.do?{urlencode(params)}"

    def get_cookies(self):
        return {}

    def parse(self, response):
        data = json.loads(response.text)
        car_list = data.get("object", {}).get("list", [])

        if not car_list:
            return

        for car in car_list:
            yield KcarScraperItem(
                api_id=car.get("v_carcd"),
                brand=car.get("xc_mkco_nm"),
                model=car.get("xc_vcl_brnd_nm"),
                year=car.get("v_pyy_yy"),
                mileage=car.get("n_dvml"),
                color=car.get("v_clrcd_nm"),
                finish=car.get("n_new_vcl_prc"),
                engine=car.get("v_fuelcd_nm"),
                grade=car.get("xc_vcl_grd_nm"),
                equip=None,
                drive=None,
                engine_volume=car.get("n_exhu_qty"),
                transmission=car.get("v_gboxcd_nm"),
                body_type=car.get("xc_vctp_nm"),
                photos=[f'https://www.autoinside.co.kr/shCardImg/{car.get("v_imgnm")}'],
                rate=None,
                month=None,
                power_volume=None,
                body_brand=None,
                lot=None,
                auction="autoinside"
            )

        self.page += 1

        if self.page <= self.max_pages:
            yield scrapy.Request(self.build_url(self.page), callback=self.parse, cookies=self.get_cookies())
