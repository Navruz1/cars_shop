import uuid
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.users.models import User, AuthLog
from apps.users.helpers import log_auth_action, PHONE_REGEX

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, required=True)
    phone_number = serializers.CharField(required=True, validators=[PHONE_REGEX])

    class Meta:
        model = User
        fields = ['first_name', 'phone_number', 'password', 'role']

    def validate_phone_number(self, value):
        if User.objects.filter(phone_number__iexact=value).exists():
            raise serializers.ValidationError(_('Phone number already in use.'))
        return value

    def validate_username(self, value):
        if value == '' or None:
            raise serializers.ValidationError(_('Username must not be empty.'))

        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(_('Username already used.'))

        return value

    def create(self, validated_data):
        request = self.context.get('request')
        user = User(
            first_name=validated_data['first_name'],
            phone_number=validated_data['phone_number'],
            username=str(uuid.uuid4())[:30],
            date_joined=timezone.now()
        )
        user.set_password(validated_data['password'])
        user.save()

        log_auth_action(user, AuthLog.ActionChoices.REGISTER, request, metadata={'info': 'User is registered'})
        return user
