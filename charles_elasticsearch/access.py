import os
from ujson import loads
from datetime import datetime

from sugar_odm import PostgresDBModel, Field
from sugar_api import JSONAPIMixin, TimestampMixin


class AccessStatus(PostgresDBModel, JSONAPIMixin, TimestampMixin):

    __connection__ = {
        'host': os.getenv('CHARLES_POSTGRES_HOST', 'localhost'),
        'port': os.getenv('CHARLES_POSTGRES_POST', '5432'),
        'user': os.getenv('CHARLES_POSTGRES_USER'),
        'password': os.getenv('CHARLES_POSTGRES_PASSWORD')
    }

    created = Field(type='timestamp', computed=lambda: datetime.now(), computed_empty=True, computed_type=True)
    accessed = Field(type='timestamp', computed=lambda: datetime.now(), computed_type=True)
    request = Field(type=dict)
    response = Field(type=dict)
    index = Field(required=True)


def access(handler):
    async def decorator(request, *args, **kargs):
        index = kargs.get('index')
        if not index:
            return await handler(request, *args, **kargs)
        model = await AccessStatus.find_one({ 'WHERE': f'data->>\'index\' = \'{index}\'' })
        if not model:
            model = AccessStatus({ 'index': index })
        if request.body:
            model.request = loads(request.body)
        response = await handler(request, *args, **kargs)
        if response.body:
            model.response = loads(response.body)
        await model.save()
        return response
    return decorator
