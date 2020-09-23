
"""
Celery Task Manage
"""

# Libraries
import os
from celery import Celery

# Dijango Settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Celery Settings
app = Celery('config')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    """Testing task"""
    print('Request: {0!r}'.format(self.request))
