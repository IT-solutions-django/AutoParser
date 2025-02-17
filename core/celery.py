import os 
from celery import Celery 
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings') 

app = Celery('core') 
app.config_from_object('django.conf:settings', namespace='CELERY') 
app.autodiscover_tasks() 

# app.conf.beat_schedule = {
#     'update_telegram_chats': {
#         'task': 'cars.tasks.update_korea',
#         'schedule': crontab(hour=0, minute=0),  
#     }
# }