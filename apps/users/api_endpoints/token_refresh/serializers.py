from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from apps.users.models import RefreshTokenModel

class TokenRefreshAPISerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        token_str = attrs.get('refresh_token')

        # Проверка в БД
        try:
            token_obj = RefreshTokenModel.objects.select_related('user').get(token=token_str, is_valid=True)
        except RefreshTokenModel.DoesNotExist:
            raise serializers.ValidationError(_("Invalid or expired refresh token."))

        # Проверить, не истёк ли срок годности Refresh токена
        if token_obj.expires_at and token_obj.expires_at < timezone.now():
            token_obj.is_valid = False
            token_obj.save(update_fields=['is_valid'])
            raise serializers.ValidationError({'refresh_token': _('Refresh token expired.')})

        # Проверка JWT (подпись, exp)
        try:
            jwt_refresh = RefreshToken(token_str)
        except TokenError:
            token_obj.is_valid = False
            token_obj.save(update_fields=["is_valid"])
            raise serializers.ValidationError(_("Invalid refresh token."))

        attrs['token_obj'] = token_obj
        attrs['jwt_refresh'] = jwt_refresh
        attrs['user'] = token_obj.user
        return attrs