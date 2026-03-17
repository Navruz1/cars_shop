import secrets
from typing import Literal
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator

from apps.users.models import User, Verify

# Phone Number Validate
PHONE_REGEX = RegexValidator(
    regex=r'^\+998\d{9}$',
    message=_("Only Uzbekistan numbers - phone number must start with +998 and contain 9 digits after.")
)

VerifyTypes = Literal[
    Verify.Type.PHONE,
    Verify.Type.EMAIL
]

#
def get_client_ip(request):
    """Возвращает IP клиента из запроса."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '')

#
def get_user_agent(request):
    """Возвращает User-Agent клиента из запроса."""
    return request.META.get('HTTP_USER_AGENT', '')

#
def generate_secret_number(length: int) -> str:
    """ """
    return ''.join(secrets.choice('0123456789') for _ in range(length))

def create_username(first_name):
    """first_name -> username"""
    fn_count = User.objects.first_name_count(first_name)
    return first_name if fn_count == 0 else first_name + str(fn_count + 1)


__all__ = [
    'PHONE_REGEX',
    'create_username',
    'get_client_ip',
    'get_user_agent',
    'generate_secret_number'
]
