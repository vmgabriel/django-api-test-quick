
"""
Especial Module for use of abstract petition data
"""

# Libraries
import json
from typing import Callable, List
from django.http import Http404
from rest_framework.response import Response

# Utils
from . import utils


def get_all(model: str, serializer: object, query: any):
    """Get All Data"""
    print(f'query_data - {query}')
    field_data = query['fields'].split(',') if 'fields' in query else []

    if 'id' not in field_data:
        field_data.append('id')

    serializer_class = serializer(
        utils.get_data(
            model,
            fields=field_data,
            filters=json.loads(query['filters']) if 'filters' in query else {},
            sorts=query['sorts'] if 'sorts' in query else '',
            limit=int(query['limit']) if 'limit' in query else utils.LIMIT_PAGE,
            offset=int(query['offset']) if 'offset' in query else 0
        ),
        many=True
    )
    return ({
        'message': 'Done Correctly',
        'count': utils.get_count(
            model,
            filters=json.loads(query['filters']) if 'filters' in query else {},
        ),
        'data': serializer_class.data
    })


def get_object(model: str, pk: any) -> dict:
    """Get Object Data"""
    try:
        filter_data = {
            'and': [
                {
                    'column': 'id',
                    'op': '=',
                    'value': pk,
                }
            ]
        }
        get_entities = utils.get_data(
            model,
            filters=filter_data
        )[0]
        return get_entities
    except model.DoesNotExist:
        raise Http404


def update_entity(
        model: object,
        serializer: Callable,
        data: dict,
        pk: any
) -> dict:
    """Update a new Process"""
    try:
        entity = get_object(model, pk)
        filters = {
            'and': [
                {
                    'column': 'id',
                    'op': '=',
                    'value': pk
                }
            ]
        }
        utils.update_data(model, filters, data)
        entity.update(data)
        serializer_update = serializer(entity)

        return Response({
            'message': 'Done Correctly',
            'data': serializer_update.data,
        })
    except model.DoesNotExist:
        raise Http404


def delete_entity(model: object, serializer: Callable, pk: any):
    """Delete a Data Generic"""
    try:
        entity = get_object(model, pk)
        filters = {
            'and': [
                {
                    'column': 'id',
                    'op': '=',
                    'value': pk
                }
            ]
        }
        utils.delete(model, filters)
        serializer_deleted = serializer(entity)

        return Response({
            'message': 'Done Correctly',
            'data': serializer_deleted.data,
        })
    except model.DoesNotExist:
        raise Http404
