import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "totalticketing.settings")

app = Celery("totalticketing")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
