import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'padhai_saathi.settings')
app = Celery('padhai_saathi')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()