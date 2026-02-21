from django.contrib.auth import update_session_auth_hash
from django.utils.translation import gettext_lazy as _
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from apps.users.models import RefreshToken, AuthLog
from apps.users.helpers import *
from .serializers import PasswordChangeSerializer


class PasswordChangeAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PasswordChangeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        old_password = serializer.validated_data['old_password']
        new_password = serializer.validated_data['new_password']

        if not user.check_password(old_password):
            return Response({
                "old_password": [_('Old password is incorrect')]
            })

        # Смена пароля
        user.set_password(new_password)
        user.save()

        # Инвалидация всех действующих refresh-токенов
        RefreshToken.objects.filter(user=user,is_valid=True).update(is_valid=False)

        # Обновление сессии
        update_session_auth_hash(request, user)

        # Логирование действий
        log_auth_action(
            user=user,
            action=AuthLog.ActionChoices.PASSWORD_CHANGE,
            request=request,
            metadata={"info": 'Password changed'}
        )

        return Response(
            {'detail': _('Password changes successfully')},
            status=status.HTTP_200_OK
        )

__all__ = ['PasswordChangeAPIView']