from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from apps.users.models import RefreshToken


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True)

    def validate_refresh_token(self, value):
        if not value.strip():
            raise serializers.ValidationError(_('Refresh token is required.'))
        return value