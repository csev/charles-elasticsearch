from ujson import loads

from fire_odm import PostgresDBModel, Field
from fire_api import TimestampMixin


class Access(PostgresDBModel, TimestampMixin):
    created = Field(type='timestamp', computed=lambda: datetime.now(), computed_empty=True)
    accessed = Field(type='timestamp', computed=lambda: datetime.now())
    username = Field(required=True)
    body = Field(type=dict, required=True)


def access(handler):
    async def decorator(request, *args, **kargs):
        index = kargs.get('index', 'administrator')
        model = await Access.find_one({ 'WHERE': f'data->>\'username\' = \'{index}\'' })
        if not model:
            model = await Access.add({ 'username': index })
        model.body = loads(request.body)
        await model.save()
        return await handler(request, *args, **kargs)
    return decorator
