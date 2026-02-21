from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        required=True, write_only=True, style={'input_type': 'password'}
    )
    new_password = serializers.CharField(
        required=True, write_only=True, style={'input_type': 'password'}
    )

    def validate_new_password(self, value):
        validate_password(value)
        old_password = self.initial_data.get('old_password')
        if old_password == value:
            raise serializers.ValidationError({
                "new_password": [_('Enter a new password')]
            })
        return value