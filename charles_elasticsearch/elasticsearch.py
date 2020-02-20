import os

import aiohttp
from sanic import Blueprint
from sanic.response import json, text

from sugar_api import webtoken, scope

from . access import access
from . authentication import auth


class Elasticsearch(object):

    __host__ = os.getenv('CHARLES_ELASTICSEARCH_URI', 'http://localhost:9200')
    __methods__ = [ 'OPTIONS', 'HEAD', 'GET', 'POST', 'PUT', 'PATCH', 'DELETE' ]

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

        @bp.route('/elasticsearch/', methods=cls.__methods__)
        @auth
        @access
        async def handler(*args, **kargs):
            return await cls.handler(*args, **kargs)

        @bp.route('/elasticsearch/<index>', methods=cls.__methods__)
        @auth
        @access
        async def handler(*args, **kargs):
            return await cls.handler(*args, **kargs)

        @bp.route('/elasticsearch/<index>/<path:path>', methods=cls.__methods__)
        @auth
        @access
        async def handler(*args, **kargs):
            return await cls.handler(*args, **kargs)

        return bp

    @classmethod
    async def handler(cls, request, index='', path='', token=None):
        uri = f'{cls.__host__}/{index}/{path}' # Elasticsearch collapses // to /
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        async with aiohttp.ClientSession() as session:
            async with session.request(request.method, uri, data=request.body, headers=headers) as response:
                try:
                    return json(await response.json())
                except aiohttp.ContentTypeError:
                    return text(await response.text())
