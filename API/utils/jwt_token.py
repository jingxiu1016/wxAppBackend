from django.conf import settings
import jwt
import datetime


def create_token(payload,timeout=1):
    salt = settings.SECRET_KEY
    headers = {
        'typ': 'jwt',
        'alg': 'HS256'
    }
    payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(minutes=timeout)
    token = jwt.encode(payload=payload,key=salt,algorithm="HS256",headers=headers).decode('utf-8')
    return token