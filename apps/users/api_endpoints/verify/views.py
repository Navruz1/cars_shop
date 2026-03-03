from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView

from .serializers import VerifyOTPSerializer, GetOTPByNumberSerializer
from apps.users.helpers import MyTokenManager, OTPManager

# Получение OTP через номер
class GetOTPByNumberView(CreateAPIView):
    serializer_class = GetOTPByNumberSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        otp_obj = OTPManager.create_otp(user)

        response_data = {
            "message": "OTP generated successfully",
            "phone_number": user.phone_number,
            "otp_expires_at": otp_obj.expires_at,
        }
        if settings.DEBUG:
            response_data['otp_code'] = otp_obj.code

        return Response(response_data, status=status.HTTP_201_CREATED)

# Ввод одноразового кода (OTP)
class VerifyOTPAPIView(CreateAPIView):
    serializer_class = VerifyOTPSerializer

    def perform_create(self, serializer):
        otp = serializer.otp_obj
        otp.is_used = True  # "Этот OTP уже использован"
        otp.save(update_fields=["is_used"])

        # Активация аккаунта
        user = serializer.user
        user.is_active = True
        user.save(update_fields=["is_active"])

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        # Создание токенов
        token_obj = MyTokenManager.generate_for_user(serializer.user, request)

        self.perform_create(serializer)
        return Response({
            "access_token": token_obj.access_token,
            "refresh_token": token_obj.token,
            "token_type": "Bearer",
            "expires_in": int(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds())
        }, status=status.HTTP_200_OK)


