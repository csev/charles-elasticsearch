import os

import aiohttp
from sanic import Blueprint
from sanic.response import json, text


class Elasticsearch(object):

    __host__ = os.getenv('FIRE_ELASTICSEARCH_URI', 'http://localhost:9200')

    @classmethod
    def set_host(cls, uri):
        cls.__host__ = uri

    @classmethod
    def get_host(cls):
        return cls.__host__

    @classmethod
    def resource(cls, *args, **kargs):

        if not len(args) > 0:
            args = [ 'elasticsearch' ]

        bp = Blueprint(*args, **kargs)

        @bp.route('/elasticsearch/')
        async def handler(*args, **kargs):
            return await cls.handler(*args, **kargs)

        @bp.route('/elasticsearch/<index>', methods=[ 'OPTIONS', 'HEAD', 'GET', 'POST', 'PUT', 'PATCH', 'DELETE' ])
        async def handler(*args, **kargs):
            return await cls.handler(*args, **kargs)

        @bp.route('/elasticsearch/<index>/<path:path>', methods=[ 'OPTIONS',  'HEAD', 'GET', 'POST', 'PUT', 'PATCH', 'DELETE' ])
        async def handler(*args, **kargs):
            return await cls.handler(*args, **kargs)

        return bp

    @classmethod
    async def handler(cls, request, index='', path=''):
        uri = f'{cls.__host__}/{index}/{path}'
        async with aiohttp.ClientSession() as session:
            async with session.request(request.method, uri) as response:
                try:
                    return json(await response.json())
                except:
                    return text(await response.text())
