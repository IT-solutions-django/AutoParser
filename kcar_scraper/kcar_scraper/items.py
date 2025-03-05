# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class KcarScraperItem(scrapy.Item):
    api_id = scrapy.Field()
    brand = scrapy.Field()
    model = scrapy.Field()
    year = scrapy.Field()
    mileage = scrapy.Field()
    color = scrapy.Field()
    finish = scrapy.Field()
    engine = scrapy.Field()
    grade = scrapy.Field()
    equip = scrapy.Field()
    drive = scrapy.Field()
    engine_volume = scrapy.Field()
    transmission = scrapy.Field()
    body_type = scrapy.Field()
    photos = scrapy.Field()
    rate = scrapy.Field()
    lot = scrapy.Field()
    power_volume = scrapy.Field()
    month = scrapy.Field()
    body_brand = scrapy.Field()
    auction = scrapy.Field()
