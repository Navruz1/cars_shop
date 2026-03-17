from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .models import User, EmailVerify, PhoneVerify, RefreshTokenModel as RTModel
from .services import TokenService

# GET List
class UsersListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'username', 'phone_number', 'email', 'role', 'is_active']


class TokenRefreshBaseSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True, write_only=True)

    def validate_token(self, value):
        # Проверка в БД
        token_obj = RTModel.objects.by_refresh(value)
        if not token_obj:
            raise serializers.ValidationError(
                _("Invalid or expired refresh token."))

        # Проверить, не истёк ли срок годности Refresh токена
        if token_obj.expired():
            TokenService.invalidate(token_obj)
            raise serializers.ValidationError(
                _('Refresh token expired.'))

        return token_obj


# OTP Verify Serializer
class VerifyBaseSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=settings.OTP_INPUT_LENGTH, required=True)

    def validate_code(self, value): # Нужно переопределять
        return value

#
class VerifySerializerService:
    @staticmethod
    def user_validate(user, data):
        if settings.DEBUG:
            if not user:
                raise serializers.ValidationError(
                    _("User with this %(field)s not found.") % {'field': data})  # Пользователя с таким номером не существует

            if user.is_active:
                raise serializers.ValidationError(
                    _("User already verified."))  # Пользователь уже активен
        else:
            if not user:
                raise serializers.ValidationError(
                    _("%(field)s error.") % {'field': data})

    @staticmethod
    def code_validate(code_obj):
        if settings.DEBUG:
            if not code_obj:
                raise serializers.ValidationError(
                    _("OTP not found."))  # Неверный код

            if code_obj.expired():
                raise serializers.ValidationError(
                    _("OTP expired."))  # Код просрочен

            if code_obj.is_used:
                raise serializers.ValidationError(
                    _("OTP already used."))  # Код уже был применён
        else:
            if not code_obj or code_obj.expired() or code_obj.is_used:
                raise serializers.ValidationError(
                    _("OTP Error."))


