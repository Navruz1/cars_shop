from rest_framework import serializers

from apps.users.models import User, PhoneVerify, EmailVerify
from apps.users.serializers import (
    VerifyBaseSerializer as VBSerializer,
    VerifySerializerService as VSService)
from apps.users.helpers import PHONE_REGEX


# Получение OTP кода через номер
class GetOTPByPhoneSerializer(serializers.Serializer):
    """Получение OTP через телефон номер"""
    phone_number = serializers.CharField(max_length=13, required=True, validators=[PHONE_REGEX])

    def validate(self, attrs):
        user = User.objects.by_phone(attrs['phone_number'])

        VSService.user_validate(user, 'Phone number')

        attrs['user'] = user
        return attrs


# Ввод одноразового кода (OTP)
class VerifyOTPSerializer(GetOTPByPhoneSerializer, VBSerializer):
    """Поле code наследуется из VerifyBaseSerializer"""

    def validate(self, attrs):
        otp_obj = PhoneVerify.objects.by_code(attrs['code'])

        VSService.code_validate(otp_obj)

        attrs['otp_obj'] = otp_obj
        return attrs