from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView

from .serializers import ConfirmEmailOTPSerializer, VerifyEmailOTPSerializer
from apps.users.models import User, Verify
from apps.users.services.verify import verify_by, after_verify

# Генерация OTP
class GetOTPByEmailView(CreateAPIView):
    serializer_class = VerifyEmailOTPSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        response_data = verify_by(
            Verify.Type.EMAIL,
            serializer.validated_data
        )

        return Response(response_data, status=status.HTTP_201_CREATED)

# Ввод одноразового кода (OTP)
class VerifyEmailAPIView(CreateAPIView):
    serializer_class = ConfirmEmailOTPSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        otp = serializer.validated_data['otp_obj']
        user = User.objects.by_id(otp.user_id)

        if not user.email:
            user.email = otp.email
            user.save(update_fields=["email"])

        response_data = after_verify(user, otp, request)

        return Response(response_data, status=status.HTTP_200_OK)


