from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

# Phone Number Validate
PHONE_REGEX = RegexValidator(
    regex=r'^\+998\d{9}$',
    message=_("Only Uzbekistan numbers - phone number must start with +998 and contain 9 digits after.")
)

def get_client_ip(request):
    """Возвращает IP клиента из запроса."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '')

def get_user_agent(request):
    """Возвращает User-Agent клиента из запроса."""
    return request.META.get('HTTP_USER_AGENT', '')

# Create AuthLog Object
def log_auth_action(user, action, request=None, metadata=None):
    """Создаёт запись в AuthLog для действий пользователя."""
    from apps.users.models import AuthLog

    AuthLog.objects.create(
        user=user,
        action=action,
        ip_address=get_client_ip(request) if request else None,
        user_agent=get_user_agent(request) if request else '',
        metadata=metadata or {}
    )




