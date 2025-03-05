# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import logging
from cars.models import AucCars, AucCarsPhoto
from asgiref.sync import sync_to_async


@sync_to_async
def save_car_data(item):
    try:
        car_obj, created = AucCars.objects.update_or_create(
            api_id=item["api_id"],
            defaults={
                "brand": item["brand"] or "Не определено",
                "model": item["model"] or "Не определено",
                "year": item["year"] or 0,
                "mileage": int(float(item["mileage"])) if item["mileage"] else 0,
                "toll": -1,  # FIXME: заменить на calc_toll
                "transmission": item["transmission"] or "Не определено",
                "engine_volume": item["engine_volume"] or "Не определено",
                "drive": item["drive"] or "Не определено",
                "color": item["color"] or "Не определено",
                "rate": item["rate"] or "Не определено",
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
                "auction": item["auction"]
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
