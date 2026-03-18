from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView

from .serializers import ConfirmPhoneOTPSerializer, VerifyPhoneOTPSerializer
from apps.users.models import Verify
from apps.users.services.verify import verify_by, after_verify

# Генерация OTP
class GetOTPByNumberView(CreateAPIView):
    serializer_class = VerifyPhoneOTPSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        response_data = verify_by(
            Verify.Type.PHONE,
            serializer.validated_data)

        return Response(response_data, status=status.HTTP_201_CREATED)


# Ввод одноразового кода (OTP)
class VerifyOTPAPIView(CreateAPIView):
    serializer_class = ConfirmPhoneOTPSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        response_data = after_verify(
            serializer.validated_data['user'],
            serializer.validated_data['otp_obj'],
            request=request
        )

        return Response(response_data, status=status.HTTP_200_OK)


