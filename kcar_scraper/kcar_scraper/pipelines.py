# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import logging
from cars.models import AucCars, AucCarsPhoto, CountryModels
from asgiref.sync import sync_to_async
from cars.sub_fun_2 import calc_price


@sync_to_async(thread_sensitive=True)
def save_car_data(item):
    try:
        try:

            if item["engine"] and item["engine"] in ['전기']:
                toll = -1

            elif item["engine"] and item["engine"] in ['LPG+가솔린', '디젤+전기', '수소', '가솔린+전기', 'LPG+전기', 'LPG', '가솔린+LPG', '수소+전기', '기타', '가솔린/LPG겸용',
                              '가솔린 하이브리드', '디젤 하이브리드']:
                if item["finish"] and item["finish"] not in ['0', 0] and item["year"] and item["year"] not in [0, '0'] and item["engine_volume"] and item["engine_volume"] not in ['0', 0]:
                    detailed_calculation = calc_price(int(item["finish"]) * 1000, int(item["year"]), int(item["engine_volume"]), 'korea', 3)
                    toll = detailed_calculation['total']
                else:
                    toll = -1

            elif item["engine"]:
                if item["finish"] and item["finish"] not in ['0', 0] and item["year"] and item["year"] not in [0, '0'] and item["engine_volume"] and item["engine_volume"] not in ['0', 0]:
                    detailed_calculation = calc_price(int(item["finish"]) * 1000, int(item["year"]), int(item["engine_volume"]), 'korea')
                    toll = detailed_calculation['total']
                else:
                    toll = -1

            else:
                toll = -1

        except Exception as e:
            toll = -1

        if item["brand"]:
            country = CountryModels.objects.filter(brand=item["brand"]).first()
        else:
            country = None

        car_obj, created = AucCars.objects.update_or_create(
            api_id=item["api_id"],
            defaults={
                "brand": item["brand"] or "Не определено",
                "model": item["model"] or "Не определено",
                "year": item["year"] or 0,
                "mileage": int(float(item["mileage"])) if item["mileage"] else 0,
                "toll": toll,
                "transmission": item["transmission"] or "Не определено",
                "engine_volume": item["engine_volume"] or "Не определено",
                "drive": item["drive"] or "Не определено",
                "color": item["color"] or "Не определено",
                "rate": item["rate"] or "Нет",
                "finish": item["finish"] or "Не определено",
                "power_volume": item["power_volume"],
                "is_active": True,
                "lot": item["lot"] or "Не определено",
                "engine": item["engine"],
                "month": item["month"],
                "grade": item["grade"],
                "equip": item["equip"],
                "body_type": item["body_type"],
                "body_brand": item["body_brand"],
                "auction": item["auction"],
                "brand_country": country
            }
        )

        if created and item.get("photos"):
            for url in item["photos"]:
                photo, _ = AucCarsPhoto.objects.get_or_create(url=url)
                car_obj.photos.add(photo)

        logging.info(f"Машина {item['api_id']} успешно сохранена")
    except Exception as e:
        logging.error(f"Ошибка при сохранении {item['api_id']}: {e}")


class KcarScraperPipeline:
    async def process_item(self, item, spider):
        await save_car_data(item)
        return item
