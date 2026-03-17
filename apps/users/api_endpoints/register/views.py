from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from apps.users.services import UserService, AuthLogService
from .serializers import RegisterSerializer

class RegisterAPIView(CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = UserService.register_user(serializer.validated_data)

        AuthLogService.log(user, AuthLogService.Action.REGISTER, request)

        return Response(
            {
                "id": user.id,
                "username": user.username,
                "phone_number": user.phone_number,
                "email": user.email or ""
            },
            status=status.HTTP_200_OK
        )


