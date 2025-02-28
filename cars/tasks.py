from celery import shared_task
from .services import parse_kcar


@shared_task
def update_korea():
    from .auc_parser import parse_korea
    parse_korea()


@shared_task 
def update_kcar(): 
    parse_kcar()
