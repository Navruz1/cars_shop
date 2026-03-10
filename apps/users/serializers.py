from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .models import User, RefreshTokenModel as RTModel
from .services import TokenService

# GET List
class UsersListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'username', 'email', 'phone_number', 'role', 'is_active']


class TokenRefreshBaseSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True, write_only=True)

    def validate_token(self, value):
        # Проверка в БД
        token_obj = RTModel.objects.by_refresh(value)
        if not token_obj:
            raise serializers.ValidationError(_("Invalid or expired refresh token."))

        # Проверить, не истёк ли срок годности Refresh токена
        if token_obj.expired():
            TokenService.invalidate(token_obj)
            raise serializers.ValidationError(_('Refresh token expired.'))

        return token_obj

