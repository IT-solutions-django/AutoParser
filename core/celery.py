import os 
from celery import Celery 
from celery.schedules import crontab
from core.settings import CELERY_BROKER_URL


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings') 

app = Celery(
    'core'
) 
app.config_from_object('django.conf:settings', namespace='CELERY') 
app.autodiscover_tasks()

import kcar_scraper.kcar_scraper.tasks

app.conf.beat_schedule = {
    'update_jpy_daily': {
        'task': 'currencies.tasks.update_jpy_task',
        'schedule': crontab(hour=11, minute=0),  
    },
    'update_krw_daily': {
        'task': 'currencies.tasks.update_krw_task',
        'schedule': crontab(hour=11, minute=0),
    },
    'update_cny_daily': {
        'task': 'currencies.tasks.update_cny_task',
        'schedule': crontab(hour=11, minute=0),
    },
    'update_eur_and_usd_daily': {
        'task': 'currencies.tasks.update_eur_and_usd_task',
        'schedule': crontab(hour=11, minute=0),
    },
    'run_spiders_daily': {
        'task': 'kcar_scraper.kcar_scraper.tasks.run_spiders_task',
        'schedule': crontab(minute=20, hour=12),
    },
}