from django.http import JsonResponse
from django.contrib.auth import get_user_model
import json

from utilities.jwt_utils import decode_jwt_token

User = get_user_model()


class JWTAuthenticationMixin:
    """Mixin to handle JWT authentication"""

    def dispatch(self, request, *args, **kwargs):
        # Skip authentication for public endpoints
        if self.is_public_endpoint(request):
            return super().dispatch(request, *args, **kwargs)

        # Get token from Authorization header
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        if not auth_header:
            return JsonResponse({"error": "Authorization header required"}, status=401)

        try:
            # Extract token from "Bearer <token>"
            token_type, token = auth_header.split(" ")
            if token_type.lower() != "bearer":
                return JsonResponse({"error": "Invalid token type"}, status=401)

            # Decode token and get user
            user = decode_jwt_token(token)
            request.user = user

        except ValueError:
            return JsonResponse(
                {"error": "Invalid authorization header format"}, status=401
            )
        except Exception as e:
            if "expired" in str(e).lower():
                return JsonResponse({"error": "Token has expired"}, status=401)
            return JsonResponse({"error": "Invalid token"}, status=401)

        return super().dispatch(request, *args, **kwargs)

    def is_public_endpoint(self, request):
        """Override this method to define public endpoints"""
        return False
