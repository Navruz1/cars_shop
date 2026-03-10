from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.users.models import User, VerifyOTP
from apps.users.helpers import PHONE_REGEX

# Получение OTP кода через номер
class GetOTPByNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=13, validators=[PHONE_REGEX], required=True)

    def validate_phone_number(self, value):
        if not User.objects.by_phone(value):
            raise serializers.ValidationError(_("Phone number error."))
        return value

# Ввод одноразового кода (OTP)
class VerifyOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=13, required=True, validators=[PHONE_REGEX])
    code = serializers.CharField(max_length=8, required=True)

    def validate(self, attrs):
        user = User.objects.by_phone(attrs['phone_number'])
        otp_obj = VerifyOTP.objects.by_code(attrs['code'])

        if settings.DEBUG:
            if not user:
                raise serializers.ValidationError(
                    _("User with this number not found."))  # Пользователя с таким номером не существует

            if user.is_active:
                raise serializers.ValidationError(
                    _("User already verified."))  # Пользователь уже активен

            if not otp_obj:
                raise serializers.ValidationError(
                    _("OTP not found."))  # Неверный код

            if otp_obj.expired():
                raise serializers.ValidationError(
                    _("OTP expired."))  # Код просрочен

            if otp_obj.is_used:
                raise serializers.ValidationError(
                    _("OTP already used."))  # Код уже был применён
        else:
            if not user:
                raise serializers.ValidationError(
                    _("Phone number Error."))

            if not otp_obj or otp_obj.expired() or otp_obj.is_used:
                raise serializers.ValidationError(
                    _("OTP Error."))

        attrs['user'] = user
        attrs['otp_obj'] = otp_obj
        return attrs


