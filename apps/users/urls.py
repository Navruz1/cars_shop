from django.urls import path
from .views import UsersListAPIView
from . import api_endpoints

urlpatterns = [
    path('', UsersListAPIView.as_view(), name='users_list'),
    path('login/', api_endpoints.LoginAPIView.as_view(), name='users_login'),
    path('logout/', api_endpoints.LogoutAPIView.as_view(), name='users_logout'),
    path('register/', api_endpoints.RegisterAPIView.as_view(), name='users_register'),
    path('token_refresh/', api_endpoints.TokenRefreshAPIView.as_view(), name='users_token_refresh'),
    path('password_change/', api_endpoints.PasswordChangeAPIView.as_view(), name='users_password_change')


]