"""
Task Asyncronus
"""

# Libraries
import csv
from celery import shared_task
from django.conf import settings

# serializer
from . import serializers


@shared_task
def create_massive(file_path: str):
    print(f'route of file 1 - {settings.BASE_DIR}')
    print(f'{settings.BASE_DIR}{file_path}')
    serializer = serializers.ClientSerializer
    with open(f'{settings.BASE_DIR}{file_path}') as f:
        reader = csv.reader(f)
        for row in reader:
            print('Creating - ', row)
            new_user = serializer(data=row)
            if new_user.is_valid():
                row['id'] = new_user.create(row)
                print('Created with Id - ', row['id'])
            print('Is not Valid -', row['id'])

            
@shared_task
def create_one_data_later(data: dict):
    print(f'data - {data}')
    serializer = serializers.ClientSerializer
    new_user = serializer(data=data)
    if new_user.is_valid():
        id = new_user.create(data)
        print('Created with Id - ', id)
    else:
        print('Is not Valid -', data)
