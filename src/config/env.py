"""
Enviroment Manage
"""

# Libraries
import os
from dotenv import load_dotenv
load_dotenv()

env = {
    'CELERY_BROKER_URL': os.getenv('CELERY_BROKER_URL'),
    'CELERY_BROKER_BACKEND': os.getenv('CELERY_BROKER_BACKEND'),
    'TIME_ZONE': os.getenv('TIME_ZONE'),
}
