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