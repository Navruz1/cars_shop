from datetime import timedelta
from django.conf import settings
from django.utils import timezone as django_timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.users.models import Verify, PhoneVerify, EmailVerify
from apps.users.helpers import VerifyTypes, generate_secret_number

def generate_numeric_otp(length: int = 6) -> str:
    """length no more 8, else DB error"""
    for _ in range(100):
        code = generate_secret_number(length)
        if not PhoneVerify.objects.by_code(code) and not EmailVerify.objects.by_code(
                code):  # Проверка отсутствия кода в БД
            return code

    raise serializers.ValidationError('Failed to generate unique OTP.')  # Если со 100 попыток не удалось сгенерировать OTP-код
    # raise Exception('Failed to generate unique otp')


def create_otp(data: str, verify_type: VerifyTypes = Verify.Type.PHONE, user_id=None) -> Verify:  # , purpose) -> VerifyOTP:
    """Сохраняет OTP в БД и возвращает объект класса VerifyOTP"""
    code = generate_numeric_otp(settings.OTP_INPUT_LENGTH)
    expires_at = django_timezone.now() + timedelta(minutes=2)

    if verify_type == Verify.Type.PHONE:
        return PhoneVerify.objects.create(phone_number=data, code=code, expires_at=expires_at)

    elif verify_type == Verify.Type.EMAIL:
        return EmailVerify.objects.create(user_id=user_id, email=data, code=code, expires_at=expires_at)

    raise serializers.ValidationError(_('OTP create error.'))


def invalidate_otp(otp: Verify):
    otp.is_used = True  # "Этот OTP уже использован"
    otp.save(update_fields=["is_used"])