from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
# set the default Django settings module for the 'celery' program.
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "voterable.settings")

# app = Celery('voterable')
app = Celery('voterable', broker=settings.CELERY_BROKER_URL)

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

app.conf.beat_schedule = {

    'add-every-10-seconds': {
        'task': 'send-email-task',
        'schedule': 300.0,
    },

    # send email every monday at 8 a.m.
    # 'send_email_monday': {
    #     'task': 'send-email-task',
    #     'schedule': crontab(hour=8, minute=0, day_of_week=1),
    # },

}

# celery -A voterable worker -l info -P eventlet

# celery -A voterable beat -l info