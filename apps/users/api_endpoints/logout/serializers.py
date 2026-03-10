from rest_framework import serializers

from apps.users.serializers import TokenRefreshBaseSerializer


class LogoutSerializer(TokenRefreshBaseSerializer):
    refresh_token = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        token = attrs['refresh_token']
        token_obj = self.validate_token(token)

        attrs['token_obj'] = token_obj
        return attrs


