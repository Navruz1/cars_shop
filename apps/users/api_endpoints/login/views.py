from django.conf import settings
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from apps.users.services import AuthLogService, TokenService
from .serializers import LoginSerializer


class LoginAPIView(CreateAPIView):
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        # Аутентификация в сериализаторе
        user = serializer.validated_data['user']

        # Создание токенов
        token_obj = TokenService.generate_for_user(user, request)

        # Логирование
        AuthLogService.log(user, AuthLogService.Action.LOGIN, request)

        return Response(
            {
                "access_token": token_obj.access_token,
                "refresh_token": token_obj.token,
                "token_type": "Bearer",
                "expires_in": int(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds())
            },
            status=status.HTTP_200_OK
        )