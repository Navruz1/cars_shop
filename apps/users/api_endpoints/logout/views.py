from django.utils.translation import gettext_lazy as _
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import ValidationError

from apps.users.helpers import log_auth_action
from apps.users.models import RefreshToken as RefreshTokenModel, AuthLog
from .serializers import LogoutSerializer


class LogoutAPIView(CreateAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        refresh_token = serializer.validated_data['refresh_token']
        user = self.request.user

        try:
            token_obj = RefreshTokenModel.objects.get(
                user=user,
                token=refresh_token,
                is_valid=True
            )
            token_obj.delete()
        except RefreshTokenModel.DoesNotExist:
            raise ValidationError(
                _("The token not found or already invalidated.")
            )
        token_obj.is_valid = False
        token_obj.save(update_fiedls=['is_valid'])

        log_auth_action(
            user=user,
            action=AuthLog.ActionChoices.LOGOUT,
            request=self.request,
            metadata={"action": "User logged out"}
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {"detail": "Muvaffaqiyatli logout qilindi."},
            status=status.HTTP_200_OK
        )

__all__ = ['LogoutAPIView']