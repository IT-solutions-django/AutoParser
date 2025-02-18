import os 
from celery import Celery 
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings') 

app = Celery('core') 
app.config_from_object('django.conf:settings', namespace='CELERY') 
app.autodiscover_tasks() 

app.conf.beat_schedule = {
    'update_jpy_daily': {
        'task': 'currencies.tasks.update_jpy',
        # 'schedule': crontab(hour=11, minute=0),  
        'schedule': 60,  
    },
    'update_krw_daily': {
        'task': 'currencies.tasks.update_krw',
        # 'schedule': crontab(hour=11, minute=0),
        'schedule': 60,  
    },
    'update_cny_daily': {
        'task': 'currencies.tasks.update_cny',
        # 'schedule': crontab(hour=11, minute=0),
        'schedule': 60,  
    },
}