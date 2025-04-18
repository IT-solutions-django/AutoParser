from celery import shared_task


@shared_task
def update_jpy_task():
    from .services import update_jpy
    update_jpy()


@shared_task
def update_cny_task():
    from .services import update_cny
    update_cny()


@shared_task
def update_krw_task():
    from .services import update_krw
    update_krw()


@shared_task
def update_eur_and_usd_task():
    from .services import update_eur_and_usd
    update_eur_and_usd()


@shared_task 
def update_currencies_from_central_bank_task(): 
    from .services import update_all_currencies_from_central_bank 
    update_all_currencies_from_central_bank()


@shared_task 
def update_currencies_from_tks_task(): 
    from .services import update_all_currencies_from_tks 
    update_all_currencies_from_tks()