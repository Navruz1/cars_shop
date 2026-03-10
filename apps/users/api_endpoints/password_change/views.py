from django.utils.translation import gettext_lazy as _
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import update_session_auth_hash

from apps.users.models import RefreshTokenModel
from apps.users.services import AuthLogService, TokenService
from .serializers import PasswordChangeSerializer

class PasswordChangeAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PasswordChangeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        user = request.user

        # Сохранить новый пароль
        user.set_password(serializer.validated_data['new_password'])
        user.save()

        # Обновить сессии, чтобы не разлогиниться
        update_session_auth_hash(request, user)

        # # Инвалидация действующего refresh-токена
        # token_obj = RefreshTokenModel.objects.by_user(user)
        # TokenService.invalidate(token_obj)

        # Логирование действий
        AuthLogService.log(user, AuthLogService.Action.PASSWORD_CHANGE, request)

        return Response(
            {
                'detail': _('Password changes successfully')
            },
            status=status.HTTP_200_OK
        )
