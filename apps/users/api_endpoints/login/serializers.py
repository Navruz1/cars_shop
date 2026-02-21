from datetime import datetime, timezone
from django.conf import settings
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.helpers import get_client_ip, get_user_agent, log_auth_action
from apps.users.models import RefreshToken as RefreshTokenModel, AuthLog


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            username=data['phone_number'],
            password=data['password']
        )
        if not user:
            raise serializers.ValidationError(_('Invalid phone number or password.'))

        if not user.is_active:
            raise serializers.ValidationError(_('User inactive.'))

        data['user'] = user
        return data

    def create(self, validated_data):
        user = validated_data['user']
        request = self.context.get('request')
        ip = get_client_ip(request)
        user_agent = get_user_agent(request)

        # JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        expires_timestamp = refresh.payload['exp']  # epoch (UTC)
        expires_at = datetime.fromtimestamp(expires_timestamp, tz=timezone.utc)

        RefreshTokenModel.objects.create(
            user=user,
            token=refresh_token,
            ip_address=ip,
            user_agent=user_agent,
            is_valid=True,
            expires_at=expires_at,
        )

        log_auth_action(
            user=user,
            action=AuthLog.ActionChoices.LOGIN,
            request=request,
            metadata={"action": "User logged in"}
        )

        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'token_type': 'Bearer',
            'expires_in': int(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds())
        }