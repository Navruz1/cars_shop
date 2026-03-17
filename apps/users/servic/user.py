from django.utils import timezone as django_timezone

from apps.users.models import User
from apps.users.helpers import create_username

def register_user(validated_data):
    """Create inactive user"""
    user = User(
        first_name=validated_data['first_name'],
        phone_number=validated_data['phone_number'],
        username=create_username(validated_data['first_name']),
        email=validated_data['email'],
        role=validated_data['role'],
        date_joined=django_timezone.now()
    )
    user.set_password(validated_data['password'])
    user.save()
    return user

def activate_user(user: User):
    user.is_active = True
    user.save(update_fields=["is_active"])

def deactivate_user(user: User):
    user.is_active = False
    user.save(update_fields=["is_active"])