from sanic.response import json

from basicauth import decode

def basicauth(handler):
    async def decorator(request, *args, **kargs):
        index = kargs.get('index')

        if not request.token:
            return json({
                'error': 'Invalid username or password.',
                'status': 403
            }, status=403)

        try:
            username, password = decode(request.token)
        except DecodeError:
            return json({
                'error': 'Invalid username or password.',
                'status': 403
            }, status=403)

        if username == 'administrator':
            return await handler(request, *args, **kargs)

        if not username == index:
            return json({
                'error': 'You do not have permission to access this index.',
                'status': 403
            }, status=403)
        return await handler(request, *args, **kargs)
    return decorator
