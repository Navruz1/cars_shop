from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.users.models import RefreshTokenModel

class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True, write_only=True)

    def validate_refresh_token(self, value):
        if not value.strip():
            raise serializers.ValidationError(_('Refresh token is required.'))
        return value


    def validate(self, attrs):
        token = attrs.get('refresh_token')
        request = self.context['request']
        user = request.user

        # Создание access токена
        try:
            token_obj = RefreshTokenModel.objects.get(user=user, token=token, is_valid=True)
        except RefreshTokenModel.DoesNotExist:
            raise serializers.ValidationError(
                {'refresh_token': _('The token not found or already invalidated.')}
            )

        attrs['token_obj'] = token_obj
        return attrs


