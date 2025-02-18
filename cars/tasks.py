from .auc_parser import parse_china, parse_japan, parse_korea
from celery import shared_task
from .services import update_prices

@shared_task
def update_japan():
    parse_japan()

@shared_task
def update_korea():
    parse_korea()

@shared_task
def update_china():
    parse_china()

@shared_task 
def update_prices(): 
    update_prices()
