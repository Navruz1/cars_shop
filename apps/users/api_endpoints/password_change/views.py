from django.contrib.auth import update_session_auth_hash
from django.utils.translation import gettext_lazy as _
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from apps.users.models import AuthLog, RefreshTokenModel
from apps.users.helpers import log_auth_action
from .serializers import PasswordChangeSerializer

class PasswordChangeAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PasswordChangeSerializer

    def perform_create(self, serializer):
        user = self.request.user
        new_password = serializer.validated_data['new_password']

        # Сохранить новый пароль
        user.set_password(new_password)
        user.save()

        # Обновить сессии, чтобы не разлогиниться
        update_session_auth_hash(self.request, user)

        # Инвалидация всех действующих refresh-токенов
        RefreshTokenModel.objects.filter(user=user, is_valid=True).update(is_valid=False)

        # Логирование действий
        log_auth_action(user, AuthLog.ActionChoices.PASSWORD_CHANGE, self.request,
                        metadata={"info": 'Password changed successfully'})

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        old_password = serializer.validated_data['old_password']

        if not request.user.check_password(old_password):  # неверный пароль
            return Response({"old_password": [_('Old password is incorrect')]}, status=status.HTTP_400_BAD_REQUEST)

        # Сохранение пароля
        self.perform_create(serializer)

        return Response(
            {'detail': _('Password changes successfully')},
            status=status.HTTP_200_OK
        )

__all__ = ['PasswordChangeAPIView']