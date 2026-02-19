import uuid
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from apps.users.models import User, AuthLog
from apps.users.helpers import log_auth_action

class RegisterSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(write_only=True, min_length=8, required=True)

    class Meta:
        model = User
        fields = ['first_name', 'phone_number', 'password']
        extra_kwargs = {
            "first_name": {"required": True},
            "phone_number": {"required": True},
            "password": {"min_length": 8}
        }

    def validate_number(self, value):
        if User.objects.filter(phone_number__iexact=value).exists():
            raise serializers.ValidationError(_('Phone number already in use.'))
        return value

    def create(self, validated_date):
        request = self.context.get('request')

        user = User(
            first_name=validated_date.get('first_name'),
            phone_number=validated_date['phone_number'],
            username=str(uuid.uuid4())[:30]
        )
        user.set_password(validated_date['password'])
        user.date_joined = timezone.now()
        user.save()

        if request:
            log_auth_action(
                user=user,
                action=AuthLog.ActionChoices.REGISTER,
                request=request,
                metadata={'info': str(_('User is registered'))}  # gettext_lazy (_) возвращает объект типа __proxy__
            )

        return user
