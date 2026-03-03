import secrets
from datetime import datetime, timedelta, timezone
from django.utils import timezone as django_timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models import User, AuthLog, VerifyOTP, RefreshTokenModel

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
    """Создаёт запись в AuthLog для логирования действий пользователя."""
    AuthLog.objects.create(
        user=user,
        action=action,
        ip_address=get_client_ip(request) if request else None,
        user_agent=get_user_agent(request) if request else '',
        metadata=metadata or {}
    )

class MyTokenManager:
    @staticmethod
    def generate_for_user(user: User, request=None) -> RefreshTokenModel:
        """Генерация и сохранение в БД Access и Refresh токенов"""
        refresh = RefreshToken.for_user(user)
        obj = RefreshTokenModel.objects.create(
            user=user,
            token=str(refresh),
            ip_address=get_client_ip(request) if request else None,
            user_agent=get_user_agent(request) if request else '',
            is_valid=True,
            expires_at=datetime.fromtimestamp(refresh.payload.get('exp'), tz=timezone.utc)
        )
        obj.access_token = str(refresh.access_token)
        return obj

class OTPManager:
    @staticmethod
    def generate_numeric_otp(length:int = 6):  # No more 8
        """OTP generate; length <= 8"""
        for _ in range(100):
            total = ''.join(secrets.choice('0123456789') for _ in range(length))  # Генерация кода
            otp_in_base = VerifyOTP.objects.filter(code=total, is_used=True).exists()
            if not otp_in_base:  # Проверка отсутствия кода в БД
                return total

        # Если со 100 попыток не удалось сгенерировать
        raise Exception('Failed to generate unique otp')

    @staticmethod
    def create_otp(user: User) -> VerifyOTP:  #, purpose) -> VerifyOTP:
        """Сохраняет OTP в БД и возвращает экземпляр класса VerifyOTP"""
        code = OTPManager.generate_numeric_otp()
        return VerifyOTP.objects.create(
            user=user,
            code=code,
            # purpose=purpose,
            expires_at=django_timezone.now() + timedelta(minutes=2)
        )

def __all__():
    return [
        'OTPManager',
        'MyTokenManager',
        'get_client_ip',
        'get_user_agent',
        'log_auth_action',
        'generate_numeric_otp',
        'PHONE_REGEX'
    ]
