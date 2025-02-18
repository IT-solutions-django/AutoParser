from . import parse_china, parse_japan, parse_korea
from celery import shared_task
from .services import update_yen


@shared_task
def update_yen():
    update_yen()

@shared_task
def update_korea():
    parse_korea()

@shared_task
def update_china():
    parse_china()

