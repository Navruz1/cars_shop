from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.users.models import User
from apps.users.helpers import PHONE_REGEX

class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    phone_number = serializers.CharField(required=True, validators=[PHONE_REGEX])
    password = serializers.CharField(write_only=True, min_length=8, required=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    role = serializers.ChoiceField(choices=User.RoleChoice.choices, default=User.RoleChoice.BUYER)

    def validate_phone_number(self, value):
        if User.objects.by_phone(value):
            raise serializers.ValidationError(_('Phone number already in use.'))
        return value



