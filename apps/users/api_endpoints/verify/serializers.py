from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.users.models import User, VerifyOTP
from apps.users.helpers import PHONE_REGEX

# Получение OTP кода через номер
class GetOTPByNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=13, required=True, validators=[PHONE_REGEX])

    def validate_phone_number(self, value):
        user = User.objects.filter(phone_number=value).first()
        if not user:
            raise serializers.ValidationError(_("User with this number not found."))  # Пользователя с таким номером не существует

        if user.is_active:
            raise serializers.ValidationError(_("User already verified."))  # Пользователь уже активен

        self.user = user
        return value

# Ввод одноразового кода (OTP)
class VerifyOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=13, required=True, validators=[PHONE_REGEX])
    code = serializers.CharField(max_length=6, required=True)

    def validate(self, attrs):
        user = User.objects.filter(phone_number=attrs['phone_number']).first()
        otp_obj = VerifyOTP.objects.filter(code=attrs['code']).first()

        if not user:
            raise serializers.ValidationError(_("User with this number not found."))  # Пользователя с таким номером не существует

        if user.is_active:
            raise serializers.ValidationError(_("User already verified."))  # Пользователь уже активен

        if settings.DEBUG:
            if not otp_obj:
                raise serializers.ValidationError(_("OTP not found."))  # Неверный код

            if not otp_obj.not_expired():
                raise serializers.ValidationError(_("OTP expired."))  # Код просрочен

            if otp_obj.is_used:
                raise serializers.ValidationError(_("OTP already used."))  # Код уже был применён
        else:
            if not otp_obj or not otp_obj.not_expired() or otp_obj.is_used:
                raise serializers.ValidationError(_("OTP Error."))

        self.otp_obj = otp_obj
        self.user = user
        return attrs


