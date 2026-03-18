from django.conf import settings
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.users.services.tokens import invalidate_refresh, generate_for_user
from .serializers import TokenRefreshAPISerializer


class TokenAccessAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = TokenRefreshAPISerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Новый access
        access = serializer.validated_data["access"]

        return Response({
            "access_token": str(access),
            "token_type": "Bearer",
            "expires_in": int(settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds())
        })


class TokenRefreshAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = TokenRefreshAPISerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token_obj = serializer.validated_data['token_obj']

        # Отменить валидность старого токена
        invalidate_refresh(token_obj)

        # Генерация нового токена
        new_token, access = generate_for_user(token_obj.user, request)

        return Response({
            "access_token": access,
            "refresh_token": new_token.token,
            "token_type": "Bearer",
            "expires_in": int(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds())
        }, status=status.HTTP_200_OK)