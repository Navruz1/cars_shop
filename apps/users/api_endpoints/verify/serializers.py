from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.users.models import User, PhoneVerify
from apps.users.serializers import VerifySerializerService as VSService
from apps.users.helpers import PHONE_REGEX


# Получение OTP кода через номер
class VerifyPhoneOTPSerializer(serializers.Serializer):
    """Получение OTP через телефон номер"""
    phone_number = serializers.CharField(max_length=13, required=True, validators=[PHONE_REGEX])

    def validate_phone_number(self, value):
        user = User.objects.by_phone(value)

        VSService.user_validate(user, 'Phone number')

        return value


# Ввод одноразового кода (OTP)
class ConfirmPhoneOTPSerializer(serializers.Serializer):
    """Подтверждение OTP"""
    phone_number = serializers.CharField(max_length=13, required=True, validators=[PHONE_REGEX])
    code = serializers.CharField(max_length=settings.OTP_INPUT_LENGTH, required=True)

    def validate(self, attrs):
        otp_obj = PhoneVerify.objects.by_code(attrs['code'])
        user = User.objects.by_phone(attrs['phone_number'])

        VSService.user_validate(user, 'Phone number')
        VSService.code_validate(otp_obj)

        if otp_obj.phone_number != attrs['phone_number']:
            raise serializers.ValidationError(_('Incorrect phone number'))

        attrs['otp_obj'] = otp_obj
        attrs['user'] = user
        return attrs