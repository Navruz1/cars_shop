from django.conf import settings
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from .serializers import LoginSerializer
from apps.users.services.authlog import log, Action
from apps.users.services.tokens import generate_for_user


class LoginAPIView(CreateAPIView):
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        # Аутентификация в сериализаторе
        user = serializer.validated_data['user']

        # Создание токенов
        token_obj, access = generate_for_user(user, request)

        # Логирование
        log(user, Action.LOGIN, request)

        return Response(
            {
                "id": user.id,
                "access_token": access,
                "refresh_token": token_obj.token,
                "token_type": "Bearer",
                "expires_in": int(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds())
            },
            status=status.HTTP_200_OK
        )