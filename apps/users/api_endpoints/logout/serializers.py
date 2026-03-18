from rest_framework import serializers

from apps.users.models import RefreshTokenModel
from apps.users.serializers import TokenRefreshSerializerService as TRSService

class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        token_str = attrs['refresh_token']
        token_obj = RefreshTokenModel.objects.by_refresh(token_str)

        TRSService.validate_token_obj(token_obj)

        attrs['token_obj'] = token_obj
        return attrs


