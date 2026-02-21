from django.urls import path
from .views import UsersListAPIView
from . import api_endpoints #.register.views import RegisterAPIView

urlpatterns = [
    path('', UsersListAPIView.as_view(), name='users_list'),
    path('login/', api_endpoints.LoginAPIView.as_view(), name='users_login'),
    path('logout/', api_endpoints.LogoutAPIView.as_view(), name='users_logout'),
    # path('register/', RegisterAPIView.as_view(), name='user_register'),
    path('register/', api_endpoints.RegisterAPIView.as_view(), name='users_register')
]