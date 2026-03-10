from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.users.models import RefreshTokenModel as RTModel
from apps.users.services import TokenService
from apps.users.serializers import TokenRefreshBaseSerializer


class TokenRefreshAPISerializer(TokenRefreshBaseSerializer):
    refresh_token = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        token = attrs['refresh_token']

        token_obj = self.validate_token(token)

        new_access = TokenService.new_access(token)

        if not new_access:
            TokenService.invalidate(token_obj)
            raise serializers.ValidationError(_("Invalid refresh token."))

        attrs['token_obj'] = token_obj
        attrs['new_access'] = new_access
        attrs['user'] = token_obj.user
        return attrs