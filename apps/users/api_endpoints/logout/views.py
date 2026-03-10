from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.users.services import AuthLogService, TokenService
from .serializers import LogoutSerializer

class LogoutAPIView(CreateAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        TokenService.invalidate(serializer.validated_data['token_obj'])

        AuthLogService.log(
            user=self.request.user,
            action=AuthLogService.Action.LOGOUT,
            request=self.request
        )

        return Response({
                "detail": _("Successfully logged out.")
            },
            status=status.HTTP_200_OK
        )

