from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.users.models import RefreshTokenModel
from apps.users.serializers import TokenRefreshSerializerService as TRSService
from apps.users.services.tokens import new_access, invalidate_refresh

class TokenRefreshAPISerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        token_obj = RefreshTokenModel.objects.by_refresh(attrs['refresh_token'])

        TRSService.validate_token_obj(token_obj)

        access = new_access(token_obj)
        if not access:
            invalidate_refresh(token_obj)
            raise serializers.ValidationError(_("Invalid refresh token."))

        attrs['token_obj'] = token_obj
        attrs['access'] = access
        return attrs