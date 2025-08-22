

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from datetime import datetime, timezone
from django.http import JsonResponse
User = get_user_model()

def generate_jwt_token(user):
    """Generate JWT token for user"""
    payload = {
        'user_id': user.id,
        'username': user.username,
        'exp': datetime.now(timezone.utc) + settings.JWT_EXPIRATION_DELTA,
        'iat': datetime.now(timezone.utc)

    }
    
    token = jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    
    return token


def verify_jwt(request):
    """Verify JWT token from request"""
    auth_header = request.META.get('HTTP_AUTHORIZATION', '')
    
    if not auth_header.startswith('Bearer '):
        return None, JsonResponse({'error': 'Invalid authorization header'}, status=401)
    
    token = auth_header.split(' ')[1]
    
    try:
        payload = jwt.decode(
            token, 
            settings.JWT_SECRET_KEY, 
            algorithms=[settings.JWT_ALGORITHM],
            options={"require": ["exp", "iat"]}
        )
        return payload, None
    except jwt.ExpiredSignatureError:
        return None, JsonResponse({'error': 'Token has expired'}, status=401)
    except jwt.InvalidTokenError as e:
        return None, JsonResponse({'error': f'Invalid token: {str(e)}'}, status=401)


def decode_jwt_token(token):
    """Decode JWT token and return user"""
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        
        user_id = payload.get('user_id')
        if user_id:
            user = User.objects.get(id=user_id)
            return user
    except jwt.ExpiredSignatureError:
        raise Exception('Token has expired')
    except jwt.InvalidTokenError:
        raise Exception('Invalid token')
    except User.DoesNotExist:
        raise Exception('User not found')
    
    return None