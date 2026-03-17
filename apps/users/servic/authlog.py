from apps.users.models import User, AuthLog
from apps.users.helpers import get_client_ip, get_user_agent

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

def log(user: User, action, request=None, metadata=None):
    """Example: AuthLogService.log(user=user, action=AuthLogService.Action.REGISTER, request=request)"""
    AuthLog.objects.create(
        user=user,
        action=action,
        ip_address=get_client_ip(request) if request else None,
        user_agent=get_user_agent(request) if request else '',
        metadata=metadata or DEFAULT_METADATA.get(action, {})
    )