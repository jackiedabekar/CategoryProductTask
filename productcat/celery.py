import os
from celery import Celery
from productcat.settings import CELERY_BROKER_URL, CELERY_RESULT_BACKEND

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'productcat.settings')

celery_app = Celery('productcat', broker = CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
celery_app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
celery_app.autodiscover_tasks()