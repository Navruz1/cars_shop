from django.conf import settings
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from apps.users.helpers import get_client_ip, get_user_agent, log_auth_action
from apps.users.models import RefreshTokenModel
from .serializers import TokenRefreshAPISerializer

class TokenRefreshAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = TokenRefreshAPISerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token_obj = serializer.validated_data['token_obj']

        # Отменить валидность старого токена
        token_obj.is_valid = False
        token_obj.save(update_fields=['is_valid'])

        # Генерация нового токена
        new_token = RefreshTokenModel.generate_for_user(
            user=serializer.validated_data['user'],
            ip_address=get_client_ip(request),
            user_agent=get_user_agent(request),
        )

        return Response({
            "access_token": new_token.access_token,
            "refresh_token": new_token.tpken,
            "token_type": "Bearer",
            "expires_in": int(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds())
        }, status=status.HTTP_200_OK)


__all__ = ['TokenRefreshAPIView']