
from django.urls import path

from authentication.views import LoginApiView, RegisterApiView


urlpatterns = [

     path("register/", RegisterApiView.as_view(), name="register-account"),
     path("login/", LoginApiView.as_view(), name="login"),
]