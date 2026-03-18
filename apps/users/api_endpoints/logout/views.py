from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import LogoutSerializer
from apps.users.services.authlog import log, Action
from apps.users.services.tokens import invalidate_refresh

class LogoutAPIView(CreateAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        invalidate_refresh(
            serializer.validated_data['token_obj'])

        log(user=self.request.user,
            action=Action.LOGOUT,
            request=self.request)

        return Response({
                "detail": _("Successfully logged out.")
            },
            status=status.HTTP_200_OK
        )

