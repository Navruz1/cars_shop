from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .models import User, RefreshTokenModel
from .services.tokens import invalidate_refresh

# GET List
class UsersListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'username', 'phone_number', 'email', 'role', 'is_active']


class TokenRefreshSerializerService:
    """Service for Serializers of Tokens API"""
    @staticmethod
    def validate_token_obj(token_obj: RefreshTokenModel):
        # Проверка в БД
        if not token_obj:
            raise serializers.ValidationError(_("Invalid or expired refresh token."))

        # Проверить, не истёк ли срок годности Refresh токена
        if token_obj.expired():
            invalidate_refresh(token_obj)
            raise serializers.ValidationError(_('Refresh token expired.'))


class VerifySerializerService:
    """OTP Verify Serializer Service"""
    @staticmethod
    def user_validate(user, data):
        if settings.DEBUG:
            if not user:
                raise serializers.ValidationError(_("User with this %(field)s not found.") % {'field': data})  # Пользователя с таким номером не существует

            if user.is_active:
                raise serializers.ValidationError(_("User already verified."))  # Пользователь уже активен
        else:
            if not user:
                raise serializers.ValidationError(_("%(field)s error.") % {'field': data})

    @staticmethod
    def code_validate(code_obj):
        if settings.DEBUG:
            if not code_obj:
                raise serializers.ValidationError(_("OTP not found."))  # Неверный код

            if code_obj.expired():
                raise serializers.ValidationError(_("OTP expired."))  # Код просрочен

            if code_obj.is_used:
                raise serializers.ValidationError(_("OTP already used."))  # Код уже был применён
        else:
            if not code_obj or code_obj.expired() or code_obj.is_used:
                raise serializers.ValidationError(
                    _("OTP Error."))


