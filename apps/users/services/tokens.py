from datetime import datetime, timezone
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from apps.users.models import User, RefreshTokenModel
from apps.users.helpers import get_client_ip, get_user_agent

def generate_for_user(user: User, request=None) -> tuple[RefreshTokenModel, str]:
    """Generate Refresh and Access tokens"""
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


def new_access(token_obj: RefreshTokenModel) -> str | None:
    """Проверка JWT (подпись, exp), возвращает Access токен"""
    try:
        refresh = RefreshToken(token_obj.token)

        if refresh['token_type'] != 'refresh':
            return None

        return str(refresh.access_token)

    except TokenError:
        return None


def invalidate_refresh(token: RefreshTokenModel):
    token.is_valid = False
    token.save(update_fields=['is_valid'])
    # try:
    #     RefreshToken(token.token)  # Инвалидируем только если JWT вообще парсится
    #
    #     token.is_valid = False
    #     token.save(update_fields=['is_valid'])
    #
    # except TokenError:
    #     pass