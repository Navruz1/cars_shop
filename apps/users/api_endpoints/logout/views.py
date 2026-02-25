from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.users.helpers import log_auth_action
from apps.users.models import AuthLog
from .serializers import LogoutSerializer

class LogoutAPIView(CreateAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        token_obj = serializer.validated_data['token_obj']
        token_obj.is_valid = False
        token_obj.save(update_fields=['is_valid'])

        log_auth_action(
            user=self.request.user,
            action=AuthLog.ActionChoices.LOGOUT,
            request=self.request,
            metadata={"action": "User logged out"}
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {"detail": _("Successfully logged out.")},
            status=status.HTTP_200_OK
        )

__all__ = ['LogoutAPIView']