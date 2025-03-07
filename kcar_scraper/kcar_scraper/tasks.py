from celery import shared_task
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from .spiders.kcar_spiders import KCarSpider
from .spiders.mpark_spiders import MparkSpider
from .spiders.charancha_spiders import CharanchaSpider
import os


@shared_task
def run_spiders_task():
    os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'kcar_scraper.settings')

    process = CrawlerProcess(get_project_settings())

    process.crawl(KCarSpider)
    process.crawl(MparkSpider)
    process.crawl(CharanchaSpider)

    process.start()
