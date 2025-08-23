import logging

from django.utils.decorators import method_decorator
import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate
from accounts.models import Account
from django.db import IntegrityError
from utilities.jwt_utils import generate_jwt_token


logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
class RegisterApiView(View):
    """User registration endpoint"""

    def post(self, request):
        try:
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")

            # Validation
            if not all([username,  password]):
                return JsonResponse(
                    {"error": "Username,  and password are required"}, status=400
                )
            # if len(password) < 6:
            #     return JsonResponse({'error': 'Password must be at least 6 characters long'}, status=400)
            
            # Check if user already exists
            if Account.objects.filter(username=username).exists():
                return JsonResponse({"error": f"Account with username {username} already exists"}, status=400)

            user = Account.objects.create_user(
                username=username, password=password
            )

            return JsonResponse(
                {
                    "message": "User registered successfully",
                    "user": {
                        "id": user.id,
                        "username": user.username,
                    },
                },
                status=201,
            )
        except IntegrityError:
            return JsonResponse({'error': 'Username already exists'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


@method_decorator(csrf_exempt, name="dispatch")
class LoginApiView(View):
    """User login endpoint"""

    def options(self, request, *args, **kwargs):
        """Handle preflight requests"""
        response = JsonResponse({})
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return response

    def post(self, request):
        try:
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")
            
            
            if not all([username, password]):
                return JsonResponse(
                    {"error": "Username and password are required"}, status=400
                )

            # Authenticate user
            user = authenticate(username=username, password=password)
            if not user:
                return JsonResponse({"error": "Invalid credentials"}, status=401)
            

            # Generate JWT token
            token = generate_jwt_token(user)

            response_data = {
                "token": token,
                "user": {
                    "id": user.id,
                    "username": user.username,
                },
            }
            
            return JsonResponse(response_data)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)