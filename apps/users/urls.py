from django.urls import path
from .api_endpoints.register.views import RegisterAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='user_register')
]