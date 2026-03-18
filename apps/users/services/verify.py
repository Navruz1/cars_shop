from django.conf import settings

from apps.users.models import User, Verify
from apps.users.helpers import VerifyTypes
from .email import send_email_otp
from .user import activate_user
from .otp import create_otp, invalidate_otp
from .tokens import generate_for_user

def verify_by(by: VerifyTypes, validated_data:dict) -> dict:
    field_name = str(by)
    value = validated_data[field_name]
    user_id = validated_data['user_id'] if by == Verify.Type.EMAIL else None

    otp_obj = create_otp(value, verify_type=by, user_id=user_id)

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
        # 'id': validated_data['user'].id,
        f"{field_name}": value,
        'otp_expires_at': otp_obj.expires_at,
    }

    if settings.DEBUG:
        response_data['otp_code'] = otp_obj.code

    return response_data


def after_verify(user:User, otp_obj:Verify, request=None) -> dict:
    # Инвалидация OTP
    invalidate_otp(otp_obj)

    # Активация аккаунта
    activate_user(user)

    # Создание токенов
    token_obj, access_token = generate_for_user(user, request)

    response_data = {
        "id": user.id,
        "access_token": access_token,
        "refresh_token": token_obj.token,
        "token_type": "Bearer",
        "expires_in": int(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds())
    }
    return response_data