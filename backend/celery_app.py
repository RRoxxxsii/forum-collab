import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('backend.core')
app.config_from_object('django.conf:settings')
app.conf.broker_url = settings.CELERY_BROKER_URL
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'delete-inactive-users': {
        'task': 'accounts.tasks.delete_inactive_accounts',
        'schedule': crontab(minute=0, hour='*/20'),
    },
}

