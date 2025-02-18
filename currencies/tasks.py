from celery import shared_task
from .services import update_jpy, update_cny, update_krw


@shared_task
def update_jpy_task():
    update_jpy()

@shared_task
def update_cny_task():
    update_cny()

@shared_task
def update_krw_task():
    update_krw()

