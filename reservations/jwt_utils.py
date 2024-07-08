import jwt
from django.conf import settings
from datetime import datetime, timedelta

def create_jwt_token(user_id):
    payload = {'user_id': user_id, 'exp': datetime.utcnow() + timedelta(hours=1)}  # Токен истекает через 1 час
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

def decode_jwt_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return payload.get('user_id')
    except jwt.ExpiredSignatureError:
        return 'Token expired. Please login again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please login again.'
