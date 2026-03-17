from datetime import datetime, timedelta, timezone
from django.conf import settings
from django.utils import timezone as django_timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from .models import User, AuthLog, RefreshTokenModel, Verify, PhoneVerify, EmailVerify
from .helpers import VerifyTypes, create_username, get_client_ip, get_user_agent, generate_secret_number
from .servic.email import send_email_otp

class UserService:
    @staticmethod
    def register_user(validated_data):
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
    def generate_for_user(user: User, request=None) -> tuple[RefreshTokenModel, str]:
        refresh = RefreshToken.for_user(user)

        obj = RefreshTokenModel.objects.create(
            user=user,
            token=str(refresh),
            ip_address=get_client_ip(request) if request else None,
            user_agent=get_user_agent(request) if request else '',
            is_valid=True,
            expires_at=datetime.fromtimestamp(
                refresh.payload.get('exp'),
                tz=timezone.utc
            )
        )

        return obj, str(refresh.access_token)

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
    def generate_numeric_otp(length: int = 6) -> str:
        """length no more 8, else DB error"""
        for _ in range(100):
            code = generate_secret_number(length)
            if not PhoneVerify.objects.by_code(code) and not EmailVerify.objects.by_code(code):  # Проверка отсутствия кода в БД
                return code

        raise serializers.ValidationError('Failed to generate unique OTP.')  # Если со 100 попыток не удалось сгенерировать OTP-код
        # raise Exception('Failed to generate unique otp')

    @classmethod
    def create_otp(cls, data:str, verify_type:VerifyTypes = Verify.Type.PHONE, user_id=None) -> Verify:  # , purpose) -> VerifyOTP:
        """Сохраняет OTP в БД и возвращает объект класса VerifyOTP"""
        code = cls.generate_numeric_otp(settings.OTP_INPUT_LENGTH)
        expires_at = django_timezone.now() + timedelta(minutes=2)

        if verify_type == Verify.Type.PHONE:
            return PhoneVerify.objects.create(phone_number=data, code=code, expires_at=expires_at)

        elif verify_type == Verify.Type.EMAIL:
            return EmailVerify.objects.create(user_id=user_id, email=data, code=code, expires_at=expires_at)

        raise serializers.ValidationError(_('OTP create error.'))


    @staticmethod
    def invalidate(otp: Verify):
        otp.is_used = True  # "Этот OTP уже использован"
        otp.save(update_fields=["is_used"])


class VerifyService(OTPService):
    @classmethod
    def verify_by(cls, by: VerifyTypes, validated_data:dict) -> dict:
        field_name = str(by)
        value = validated_data[field_name]
        user_id = validated_data['user_id'] if by == Verify.Type.EMAIL else None

        otp_obj = cls.create_otp(value, verify_type=by, user_id=user_id)

        # if by == Verify.Type.PHONE:
        #     Здесь должна быть вызвана отправка СМС с OTP на номер пользователя

        if by == Verify.Type.EMAIL:
            send_email_otp(
                email=value,
                otp_code=otp_obj.code,
                expires_at=otp_obj.expires_at,
            )

        response_data = {
            'message': 'OTP generated successfully',
            'id': validated_data['user'].id,
            f"{field_name}": value,
            'otp_expires_at': otp_obj.expires_at,
        }

        if settings.DEBUG:
            response_data['otp_code'] = otp_obj.code

        return response_data

    # @classmethod
    # def user_verified(cls, serializer, request = None) -> dict:
    #     user:User = serializer.user
    #     otp:Verify = serializer.otp_obj

    @classmethod
    def user_verified(cls, user:User, otp_obj:Verify, request=None) -> dict:
        # Инвалидация OTP
        cls.invalidate(otp_obj)

        # Активация аккаунта
        UserService.activate(user)

        # Создание токенов
        token_obj, access_token = TokenService.generate_for_user(user, request)

        response_data = {
            "access_token": access_token,
            "refresh_token": token_obj.token,
            "token_type": "Bearer",
            "expires_in": int(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds())
        }

        return response_data


