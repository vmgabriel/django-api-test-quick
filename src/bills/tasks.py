"""
Task Asyncronus
"""

# Libraries
from celery import shared_task


@shared_task
def create_massive(file_path: str):
    print('The File Path is - ', file_path)
