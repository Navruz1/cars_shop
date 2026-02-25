from django.conf import settings
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from apps.users.helpers import get_client_ip, get_user_agent, log_auth_action
from apps.users.models import RefreshTokenModel, AuthLog
from .serializers import LoginSerializer

class LoginAPIView(CreateAPIView):
    serializer_class = LoginSerializer

    def perform_create(self, serializer):
        log_auth_action(
            user=serializer.validated_data['user'],
            action=AuthLog.ActionChoices.LOGIN,
            request=self.request,
            metadata={"action": "User logged in"}
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        # Создание токенов
        token_obj = RefreshTokenModel.generate_for_user(
            user=serializer.validated_data['user'],
            ip_address=get_client_ip(request),
            user_agent=get_user_agent(request),
        )

        self.perform_create(serializer)
        return Response({
            "access_token": token_obj.access_token,
            "refresh_token": token_obj.token,
            "token_type": "Bearer",
            "expires_in": int(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds())
        }, status=status.HTTP_200_OK)


__all__ = ['LoginAPIView']