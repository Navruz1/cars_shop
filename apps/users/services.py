from datetime import datetime, timedelta, timezone
from django.conf import settings
from django.utils import timezone as django_timezone
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from .models import User, AuthLog, RefreshTokenModel, VerifyOTP
from .helpers import create_username, get_client_ip, get_user_agent, generate_secret_number

class UserService:
    @staticmethod
    def register_user(validated_data):
        user = User(
            first_name=validated_data['first_name'],
            phone_number=validated_data['phone_number'],
            username=create_username(validated_data['first_name']),
            role=validated_data['role'],
            date_joined=django_timezone.now()
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    @staticmethod
    def activate(user: User):
        user.is_active = True
        user.save(update_fields=["is_active"])


class AuthLogService:
    class Action:
        """Actions: LOGIN, LOGOUT, REGISTER, REFRESH, PASSWORD_CHANGE."""
        LOGIN = AuthLog.ActionChoices.LOGIN
        LOGOUT = AuthLog.ActionChoices.LOGOUT
        REGISTER = AuthLog.ActionChoices.REGISTER
        REFRESH = AuthLog.ActionChoices.REFRESH
        PASSWORD_CHANGE = AuthLog.ActionChoices.PASSWORD_CHANGE

    DEFAULT_METADATA = {
        Action.LOGIN: {'info': 'User logged in'},
        Action.LOGOUT: {'info': 'User logged out'},
        Action.REGISTER: {'info': 'User registered successfully'},
        Action.REFRESH: {'info': 'Tokens refreshed successfully'},
        Action.PASSWORD_CHANGE: {'info': "Password changed successfully"},
    }

    @classmethod
    def log(cls, user: User, action, request=None, metadata=None):
        """Example: AuthLogService.log(user=user, action=AuthLogService.Action.REGISTER, request=request)"""
        AuthLog.objects.create(
            user=user,
            action=action,
            ip_address=get_client_ip(request) if request else None,
            user_agent=get_user_agent(request) if request else '',
            metadata=metadata or cls.DEFAULT_METADATA.get(action, {})
        )



class TokenService:
    @staticmethod
    def generate_for_user(user: User, request=None) -> RefreshTokenModel:
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

    @staticmethod
    def new_access(token_obj: RefreshTokenModel):
        try:
            # Проверка JWT (подпись, exp)
            return RefreshToken(token_obj).access_token
        except TokenError:
            return None

    @staticmethod
    def invalidate(token: RefreshTokenModel):
        token.is_valid = False
        token.save(update_fields=['is_valid'])



class OTPService:
    @staticmethod
    def generate_numeric_otp(length:int = 6):
        """length no more 8, else DB error"""
        for _ in range(100):
            code = generate_secret_number(length)
            if not VerifyOTP.objects.by_code(code):  # Проверка отсутствия кода в БД
                return code

        # Если со 100 попыток не удалось сгенерировать
        raise Exception('Failed to generate unique otp')

    @classmethod
    def create_otp(cls, phone_number: str) -> VerifyOTP:  #, purpose) -> VerifyOTP:
        """Сохраняет OTP в БД и возвращает объект класса VerifyOTP"""
        return VerifyOTP.objects.create(
            phone_number=phone_number,
            code=cls.generate_numeric_otp(settings.OTP_INPUT_LENGTH),
            expires_at=django_timezone.now() + timedelta(minutes=2)
            # purpose=purpose,
        )

    @staticmethod
    def invalidate(otp: VerifyOTP):
        otp.is_used = True  # "Этот OTP уже использован"
        otp.save(update_fields=["is_used"])




