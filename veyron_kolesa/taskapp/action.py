from celery.task import periodic_task
from django.utils import timezone
from celery.schedules import crontab
from veyron_kolesa.taskapp.celery import app


@app.task
def periodic_just_for_lulz():
    now = timezone.now()
    print(f'Now time is - {now}')
