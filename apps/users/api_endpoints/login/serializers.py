from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(
            username=attrs['phone_number'],
            password=attrs['password']
        )

        if not user or not user.is_active:
            raise serializers.ValidationError(_('Invalid phone number or password.'))

        attrs['user'] = user
        return attrs

