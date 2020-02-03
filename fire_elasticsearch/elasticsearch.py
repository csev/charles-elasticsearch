import aiohttp
from sanic import Blueprint
from sanic.response import json


class Elasticsearch(object):

    @classmethod
    def resource(cls, *args, **kargs):

        if not len(args) > 0:
            args = [ 'elasticsearch' ]

        bp = Blueprint(*args, **kargs)

        @bp.route('/')
        async def handler(*args, **kargs):
            return await cls.handler(*args, **kargs)

        @bp.route('/<path:path>')
        async def handler(*args, **kargs):
            return await cls.handler(*args, **kargs)

        return bp

    @classmethod
    async def handler(cls, request, path=''):
        uri = f'http://192.168.99.100:9200{request.path.lstrip("/v1/elasticsearch")}'
        async with aiohttp.ClientSession() as session:
            async with session.request(request.method, uri) as response:
                return json(await response.json())
