from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView

from .serializers import VerifyOTPSerializer, GetOTPByNumberSerializer
from apps.users.services import UserService, OTPService, TokenService


# Генерация OTP
class GetOTPByNumberView(CreateAPIView):
    serializer_class = GetOTPByNumberSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        otp_obj = OTPService.create_otp(serializer.validated_data['phone_number'])

        response_data = {
            "message": "OTP generated successfully",
            "phone_number": serializer.validated_data['phone_number'],
            "otp_expires_at": otp_obj.expires_at,
        }
        if settings.DEBUG:
            response_data['otp_code'] = otp_obj.code
        else:
            # Здесь должна быть реализована отправка OTP
            # через СМС на номер пользователя
            pass

        return Response(response_data, status=status.HTTP_201_CREATED)


# Ввод одноразового кода (OTP)
class VerifyOTPAPIView(CreateAPIView):
    serializer_class = VerifyOTPSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        # Инвалидация OTP
        OTPService.invalidate(serializer.validated_data['otp_obj'])

        # Активация аккаунта
        UserService.activate(serializer.validated_data['user'])

        # Создание токенов
        token_obj = TokenService.generate_for_user(serializer.user, request)

        return Response({
            "access_token": token_obj.access_token,
            "refresh_token": token_obj.token,
            "token_type": "Bearer",
            "expires_in": int(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds())
        }, status=status.HTTP_200_OK)


