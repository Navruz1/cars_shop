from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from .serializers import RegisterSerializer
from apps.users.services.user import register_user
from apps.users.services.authlog import log, Action

class RegisterAPIView(CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = register_user(serializer.validated_data)

        log(user, Action.REGISTER, request)

        return Response({
                "id": user.id,
                "username": user.username,
                "phone_number": user.phone_number,
                "email": user.email or ""
            },
            status=status.HTTP_200_OK
        )


