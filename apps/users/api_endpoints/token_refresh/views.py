from django.conf import settings
from django.utils import timezone
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.users.helpers import MyTokenManager
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
        new_token = MyTokenManager.generate_for_user(serializer.validated_data['user'], request)

        return Response({
            "access_token": new_token.access_token,
            "refresh_token": new_token.token,
            "token_type": "Bearer",
            "expires_in": int(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds())
        }, status=status.HTTP_200_OK)


class TokenAccessAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = TokenRefreshAPISerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        jwt_refresh = serializer.validated_data["jwt_refresh"]
        token_obj = serializer.validated_data["token_obj"]

        # Новый access
        new_access = str(jwt_refresh.access_token)
        token_obj.updated_at = timezone.now()
        token_obj.save(update_fields=["updated_at"])

        return Response({
            "access_token": new_access,
            "refresh_token": token_obj.token,
            "token_type": "Bearer",
            "expires_in": int(settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds())
        })