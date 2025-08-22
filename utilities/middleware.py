import time
import logging
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware(MiddlewareMixin):
    """Custom middleware to log request details"""
    
    def process_request(self, request):
        """Start timer for request"""
        request._start_time = time.time()
    
    def process_response(self, request, response):
        """Log request details"""
        if hasattr(request, '_start_time'):
            duration = (time.time() - request._start_time) * 1000  # Convert to milliseconds
            logger.info(
                f"{request.method} {request.get_full_path()} - {response.status_code} - {duration:.2f}ms"
            )
            print(f"{request.method} {request.get_full_path()} - {response.status_code} - {duration:.2f}ms")
        
        return response