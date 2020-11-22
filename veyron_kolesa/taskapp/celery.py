import os
from celery import Celery
from django.apps import apps, AppConfig
from django.conf import settings
from celery.schedules import crontab
#
if not settings.configured:
    # set the default Django settings module for the 'celery' program.
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE", "config.settings.local"
    )  # pragma: no cover

#
#
app = Celery("veyron_kolesa", include=['veyron_kolesa.parser.advert_links', "veyron_kolesa.parser.scrape_car"])
# Using a string here means the worker will not have to
# pickle the object when using Windows.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


class CeleryAppConfig(AppConfig):
    name = "veyron_kolesa.taskapp"
    verbose_name = "Celery Config"
#
    # app.conf.beat_schedule = {
    #     # Executes at sunset in Melbourne
    #         'add-at-melbourne-sunset': {
    #         'task': 'taskapp.action.periodic_just_for_lulz',
    #         'schedule': crontab(minute="*/2"),
    #     }
    # }
# #
# # @app.task(bind=True)
# def debug_task(self):
#     print(f"Request: {self.request!r}")  # pragma: no cover
