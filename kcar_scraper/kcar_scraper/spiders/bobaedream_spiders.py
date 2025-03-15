import scrapy
from kcar_scraper.items import KcarScraperItem
from urllib.parse import urlparse, parse_qs
import re
from asgiref.sync import sync_to_async


class BobaedreamSpider(scrapy.Spider):
    name = 'bobaedream'
    auction_value = "bobaedream"

    custom_settings = {
        "DOWNLOAD_DELAY": 0.3,
        "RANDOMIZE_DOWNLOAD_DELAY": True,
        "AUTOTHROTTLE_ENABLED": True,
        "AUTOTHROTTLE_START_DELAY": 0.5,
        "AUTOTHROTTLE_MAX_DELAY": 2,
        "AUTOTHROTTLE_TARGET_CONCURRENCY": 3.0,
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }

    start_urls = ['https://www.bobaedream.co.kr/cyber/CyberCar.php?sel_m_gubun=ALL']
    max_pages = 583

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, meta={'page_number': 1})

    def parse(self, response):
        car_links = response.css('p.tit.ellipsis.video a::attr(href)').getall()
        for link in car_links:
            yield response.follow(link, self.parse_car, meta={'url': link})

        page_number = response.meta.get('page_number', 1)
        if page_number < self.max_pages:
            next_page = f"https://www.bobaedream.co.kr/cyber/CyberCar.php?sel_m_gubun=ALL&page={page_number + 1}&order=S11&view_size=70"
            yield response.follow(next_page, self.parse, meta={'page_number': page_number + 1})

    def parse_car(self, response):
        full_name_car = response.css('h3.tit::text').get(default='').strip()
        brand_car, model_car = (full_name_car.split(' ', 1) + [None])[:2]

        car_url = response.meta['url']
        parsed_url = urlparse(car_url)
        api_id = parse_qs(parsed_url.query).get('no', [None])[0]

        mileage_text = response.xpath('//th[contains(text(), "주행거리")]/following-sibling::td[1]/text()').get()
        mileage = int(re.sub(r"[^\d]", "", mileage_text))

        year_text = response.xpath('//th[contains(text(), "연식")]/following-sibling::td[1]/text()').get()
        if year_text:
            match = re.match(r"^\d+", year_text)
            year = int(match.group()) if match else 0
        else:
            year = 0

        engine_text = response.xpath('//th[contains(text(), "배기량")]/following-sibling::td[1]/text()').get()
        engine_volume = int(re.sub(r"[^\d]", "", engine_text.split("cc")[0]))

        yield KcarScraperItem(
            api_id=api_id,
            brand=brand_car,
            model=model_car,
            year=year,
            mileage=mileage,
            color=response.xpath('//th[contains(text(), "색상")]/following-sibling::td[1]/text()').get(),
            finish=response.css('span.price::text').get(),
            engine=response.xpath('//th[contains(text(), "연료")]/following-sibling::td[1]/text()').get(),
            engine_volume=engine_volume,
            transmission=response.xpath('//th[contains(text(), "변속기")]/following-sibling::td[1]/text()').get(),
            photos=response.css('ul.gallery img::attr(src)').getall(),
            auction="bobaedream",
            grade=None,
            equip=None,
            drive=response.xpath('//span[contains(text(), "구동방식")]/following-sibling::strong[@class="txt"]/text()').get(),
            body_type=None,
            rate=None,
            month=None,
            power_volume=None,
            body_brand=None,
            lot=None,
        )
