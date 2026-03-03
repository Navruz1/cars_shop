from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.users.helpers import PHONE_REGEX

class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=13, required=True, validators=[PHONE_REGEX])
    password = serializers.CharField(min_length=8, required=True, write_only=True)

    def validate(self, attrs):
        user = authenticate(
            username=attrs['phone_number'],
            password=attrs['password']
        )

        if not user:
            raise serializers.ValidationError(_('Invalid phone number or password.'))

        if not user.is_active:
            raise serializers.ValidationError(_('Account not active. Please, verify.'))

        attrs['user'] = user
        return attrs

