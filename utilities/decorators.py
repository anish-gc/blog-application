# utilities/decorators.py
from functools import wraps
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from utilities.jwt_utils import verify_jwt, decode_jwt_token

def jwt_required_func(view_func):
    """Decorator for function-based views"""
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        payload, error_response = verify_jwt(request)
        if error_response:
            return error_response
        
        try:
            auth_header = request.META.get('HTTP_AUTHORIZATION', '')
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
                user = decode_jwt_token(token)
                request.user = user
            else:
                return JsonResponse({'error': 'Invalid authorization header'}, status=401)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=401)
        
        return view_func(request, *args, **kwargs)
    
    return wrapped_view

def jwt_required_class(view_func):
    """Decorator for class-based views - direct usage"""
    @wraps(view_func)
    def wrapped_view(self, request, *args, **kwargs):
        payload, error_response = verify_jwt(request)
        if error_response:
            return error_response
        
        try:
            auth_header = request.META.get('HTTP_AUTHORIZATION', '')
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
                user = decode_jwt_token(token)
                request.user = user
            else:
                return JsonResponse({'error': 'Invalid authorization header'}, status=401)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=401)
        
        return view_func(self, request, *args, **kwargs)
    
    return wrapped_view

def jwt_required_method(view_func):
    """Decorator for use with method_decorator"""
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        payload, error_response = verify_jwt(request)
        if error_response:
            return error_response
        
        try:
            auth_header = request.META.get('HTTP_AUTHORIZATION', '')
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
                user = decode_jwt_token(token)
                request.user = user
            else:
                return JsonResponse({'error': 'Invalid authorization header'}, status=401)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=401)
        
        return view_func(request, *args, **kwargs)
    
    return wrapped_view

# Aliases for convenience
jwt_required = jwt_required_class  # For direct usage on methods
jwt_required_for_method_decorator = jwt_required_method  # For use with @method_decorator