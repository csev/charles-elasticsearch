import os, hashlib
from uuid import uuid4
from datetime import datetime

from sanic.response import json

from basicauth import decode

__secret__ = os.getenv('SHARED_SECRET', str(uuid4()))

def getexpire(date) :

    strdate = str(date)

    # 2005
    expire = strdate[2:4] + strdate[5:7]
    return int(expire)

def makepw(user, secret):

    # 2020-05-03 20:07:19.778803
    date = datetime.now()
    date = date + relativedelta(months=+3)

    expire = getexpire(date)

    # user_2005
    index = user + '_' + str(expire)

    # user_2005_asecret
    base = index + '_' + secret
    print('BASE', base)

    m = hashlib.sha256()
    m.update(base.encode())
    sig = m.hexdigest()

    # 2005_7cce7423
    pw = str(expire) + '_' + sig[0:8]
    return pw

def checkpw(user, pw, secret) :
    # 2020-05-03 20:07:19.778803
    date = datetime.now()
    expire = getexpire(date)

    pieces = pw.split('_')
    if len(pieces) != 2 : return False

    try:
        check = int(pieces[0])
    except:
        return False

    if expire > check:
        return False

    # user_2005_asecret
    base = user + '_' + str(check) + '_' + secret
    print('BASE', base)

    m = hashlib.sha256()
    m.update(base.encode())
    sig = m.hexdigest()

    # user_2005_asecret
    return sig.startswith(pieces[1])

def basic(handler):
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

        if not checkpw(username, password, __secret__):
            return json({
                'error': 'Invalid username or password.',
                'status': 403
            }, status=403)

        if not username == index:
            return json({
                'error': 'You do not have permission to access this index.',
                'status': 403
            }, status=403)

        return await handler(request, *args, **kargs)
    return decorator
