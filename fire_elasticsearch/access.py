from ujson import loads
from datetime import datetime

from fire_odm import PostgresDBModel, Field
from fire_api import TimestampMixin


class Access(PostgresDBModel, TimestampMixin):
    created = Field(type='timestamp', computed=lambda: datetime.now(), computed_empty=True, computed_type=True)
    accessed = Field(type='timestamp', computed=lambda: datetime.now(), computed_type=True)
    username = Field(required=True)
    request = Field(type=dict)
    response = Field(type=dict)


def access(handler):
    async def decorator(request, *args, **kargs):
        index = kargs.get('index')
        if not index:
            return await handler(request, *args, **kargs)
        model = await Access.find_one({ 'WHERE': f'data->>\'username\' = \'{index}\'' })
        if not model:
            model = Access({ 'username': index })
        if request.body:
            model.request = loads(request.body)
        response = await handler(request, *args, **kargs)
        if response.body:
            model.response = loads(response.body)
        await model.save()
        return response
    return decorator
