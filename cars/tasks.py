from celery import shared_task
# from .services import update_prices


@shared_task
def update_korea():
    from .auc_parser import parse_korea
    parse_korea()

# @shared_task 
# def update_prices(): 
#     update_prices()
