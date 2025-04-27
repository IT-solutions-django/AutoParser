from celery import shared_task
from .services import parse_kcar
import json
from pathlib import Path


@shared_task
def update_korea():
    from .auc_parser import parse_korea
    from .models import AucCars

    json_file = Path("cars_ids.json")

    parse_korea()

    if not json_file.exists():
        return

    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    json_car_ids = set(data.get("car_ids", []))

    db_car_ids = set(AucCars.objects.values_list("api_id", flat=True))

    cars_to_delete = list(db_car_ids - json_car_ids)

    if cars_to_delete:
        AucCars.objects.filter(api_id__in=cars_to_delete, auction='encar').delete()

    with open(json_file, "w", encoding="utf-8") as f:
        json.dump({"car_ids": []}, f, ensure_ascii=False, indent=4)


@shared_task 
def update_kcar(): 
    parse_kcar()


@shared_task
def update_encar(user_ip=None):
    from .auc_parsers_2 import fetch_catalog_car

    fetch_catalog_car(user_ip=user_ip)

