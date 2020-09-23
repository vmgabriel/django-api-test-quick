"""
Abstractu Utility for code sql pure
"""

# Libraries
from typing import List
from django.db import connection

LIMIT_PAGE = 10

def get_limit(limit: int) -> str:
    """Convert Data Limit Query"""
    return f'LIMIT {limit}'


def get_offset(limit: int, offset: int) -> str:
    """Convert Data Offset Query"""
    page = offset*limit
    print('page -', page)
    return f'OFFSET {page}'


def convert_to_order(order: str) -> str:
    """Convert to valid data order"""
    return f'{order[1:]} DESC' if order[0] == '-' else f'{order} ASC'


def get_order(orders: str) -> str:
    """Convert to Order Data"""
    orders = ','.join(list(map(convert_to_order, orders.split(','))))
    return f'ORDER BY {orders}'


def convert_operation(op: str, value: any) -> str:
    """Convert Operation Data"""
    lower_op = op.lower()
    return f'{lower_op} %s'


def convert_filter(filter_data: dict) -> str:
    """Convert a Filter"""
    column = filter_data.get('column')
    _op = filter_data.get('op')
    value = filter_data.get('value')
    return f'{column} {convert_operation(_op, value)}'


def convert_filters(filters: dict) -> str:
    """Convert_filters"""
    query_filter = ''
    and_data = filters.get('and')
    if not isinstance(and_data, list):
        if and_data:
            and_data.default = 'AND'
            query_filter += f' {convert_filters(and_data)}'
    else:
        query_filter += '('
        query_filter += ' AND '.join(list(map(convert_filter, and_data)))
        query_filter += ')'

    query_filter += ' {} '.format(
        filters.get('default') if 'default' in filters else ''
    ) \
        if filters.get('and') and filters.get('or') else ''

    or_data = filters.get('or')
    if not isinstance(or_data, list):
        if or_data:
            or_data.default = 'OR'
            query_filter += f' {convert_filters(or_data)}'
    else:
        query_filter += '('
        query_filter += ' OR '.join(list(map(convert_filter, or_data)))
        query_filter += ')'

    return query_filter


def get_values(filters: dict) -> List[any]:
    """Get Value Filter for query search"""
    print('filters - ', filters)
    data = []
    if isinstance(filters.get('and'), list):
        data += list(map(
            lambda x: x.get('value') if not x.get('op').lower() == 'like' else f"%{x.get('value')}%",
            filters.get('and')
        ))
    else:
        if filters.get('and'):
            data += get_values(filters.get('and'))

    if isinstance(filters.get('or'), list):
        data += list(map(
            lambda x: x.get('value') if not x.get('op').lower() == 'like' else f"%{x.get('value')}%",
            filters.get('or')
        ))
    else:
        if filters.get('or'):
            data += get_values(filters.get('or'))
    return data


def get_data(
        model: object,
        fields=[],
        filters={},
        sorts='',
        limit=LIMIT_PAGE,
        offset=0
):
    """Get Data Process"""
    db_table = model._meta.db_table

    values_filter = get_values(filters) \
        if 'and' in filters or 'or' in filters else []
    print('values_filter - ', values_filter)

    query = 'SELECT {} FROM {} {} {} {} {};'.format(
        ','.join(fields) if len(fields) > 1 else '*',
        db_table,
        'WHERE ' + convert_filters(filters) if 'and' in filters or 'or' in filters else '',
        get_order(sorts) if not len(sorts) == 0 else '',
        get_offset(
            limit,
            offset
        ) if not (limit == LIMIT_PAGE and offset == 0) else '',
        get_limit(limit)
    )
    print('query - ', query)
    with connection.cursor() as cursor:
        cursor.execute(query, values_filter)
        columns = [col[0] for col in cursor.description]
        print('columns - ', columns)
        rows = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]
    return rows


def update_data(model: dict, filters: dict, data: dict) -> List[any]:
    """Get Update Query"""
    print('Hi, am here')
    db_table = model._meta.db_table

    values_filter = list(data.values())
    values_filter += get_values(filters) \
        if 'and' in filters or 'or' in filters else []
    print('values_filter - ', values_filter)

    query = 'UPDATE {} SET {} WHERE {};'.format(
        db_table,
        ','.join(list(map(lambda x: f'{x} = %s', data.keys()))),
        convert_filters(filters)
    )
    print('Query - ', query)
    with connection.cursor() as cursor:
        cursor.execute(query, values_filter)
    return True


def get_count(model: object, filters={}):
    """Get Count of Data"""
    db_table = model._meta.db_table
    values_filter = get_values(filters) \
        if 'and' in filters or 'or' in filters else []

    query = 'SELECT COUNT(*) FROM {} {};'.format(
        db_table,
        'WHERE ' + convert_filters(filters) if 'and' in filters or 'or' in filters else '',
    )
    data = model.objects.raw(query)
    with connection.cursor() as cursor:
        cursor.execute(query, values_filter)
        data = cursor.fetchone()
    return data[0]


def create(model: object, serializer: object):
    """Create a new Process"""
    db_table = model._meta.db_table
    if serializer.is_valid():
        data_serialized = serializer.data

        query_insert = 'INSERT INTO {} ({}) VALUES ({}) RETURNING *;'.format(
            db_table,
            ','.join(data_serialized.keys()),
            ','.join('%s' for data in data_serialized.values())
        )
        with connection.cursor() as cursor:
            cursor.execute(query_insert, list(data_serialized.values()))
            columns = [col[0] for col in cursor.description]
            print('columns - ', columns)
            rows = [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]
        return rows[0]
    return {
        'code': 400,
        'message': 'Data not valid',
        'errors': serializer.errors
    }


def delete(model: object, filters: dict):
    """Create a new Process"""
    db_table = model._meta.db_table

    values_filter = get_values(filters) \
        if 'and' in filters or 'or' in filters else []
    print('values_filter - ', values_filter)

    query = 'DELETE FROM {} WHERE {};'.format(
        db_table,
        convert_filters(filters)
    )
    print('Query - ', query)
    with connection.cursor() as cursor:
        cursor.execute(query, values_filter)
    return True


def get_data_value_bill_user(client_id: any) -> tuple:
    """Get Data Bills of Client"""
    query = """
    SELECT b.client_id,
           c.first_name,
           c.last_name,
           c.identification,
           count(b.client_id) as bill_count
    FROM bill as b
    LEFT JOIN client as c on b.client_id = c.id
    WHERE c.id = %s
    GROUP BY
      b.client_id,
      c.first_name,
      b.client_id,
      c.last_name,
      c.identification
    """
    with connection.cursor() as cursor:
        cursor.execute(query, [client_id])
        columns = [col[0] for col in cursor.description]
        rows = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]
    return (columns, rows)
