from django.urls import path
from .views import UsersListAPIView
from . import api_endpoints

urlpatterns = [
    path('', UsersListAPIView.as_view(), name='users_list'),
    path('login/', api_endpoints.LoginAPIView.as_view(), name='login'),
    path('logout/', api_endpoints.LogoutAPIView.as_view(), name='logout'),
    path('register/', api_endpoints.RegisterAPIView.as_view(), name='users_register'),

    path('create_otp/', api_endpoints.GetOTPByNumberView.as_view(), name='otp_for_phone_number'),
    path('create_otp/email', api_endpoints.GetOTPByEmailView.as_view(), name='otp_for_email'),
    path('verify/', api_endpoints.VerifyOTPAPIView.as_view(), name='verify_by_phone_number'),
    path('verify/email', api_endpoints.VerifyEmailAPIView.as_view(), name='verify_by_email'),

    path('token_access/', api_endpoints.TokenAccessAPIView.as_view(), name='new_access_token'),
    path('token_refresh/', api_endpoints.TokenRefreshAPIView.as_view(), name='new_refresh_token'),
    path('password_change/', api_endpoints.PasswordChangeAPIView.as_view(), name='users_password_change')

]
#