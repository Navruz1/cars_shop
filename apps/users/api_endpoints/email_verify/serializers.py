from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.users.models import User, EmailVerify
from apps.users.serializers import VerifySerializerService as VSService


class VerifyEmailOTPSerializer(serializers.Serializer):
    """Получение OTP кода через почту"""
    # user = serializers.PrimaryKeyRelatedField(  # автоматически проверяет id
    #     queryset=User.objects.all()
    # )
    user_id = serializers.IntegerField()
    email = serializers.EmailField(max_length=100, required=True)

    def validate(self, attrs):
        user = User.objects.by_id(attrs['user_id'])

        VSService.user_validate(user, 'ID')

        if user.email and user.email != attrs['email']:
            raise serializers.ValidationError({
                'email': _('Incorrect email')
            })

        attrs['user'] = user
        return attrs


class ConfirmEmailOTPSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    code = serializers.CharField(max_length=settings.OTP_INPUT_LENGTH, required=True)

    def validate(self, attrs):
        user = User.objects.by_id(attrs['user_id'])
        otp_obj = EmailVerify.objects.by_code(attrs['code'])

        VSService.user_validate(user, 'ID')
        VSService.code_validate(otp_obj)

        attrs['otp_obj'] = otp_obj
        return attrs
