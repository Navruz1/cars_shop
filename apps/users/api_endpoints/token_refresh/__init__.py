"""
TokenRefreshAPI нужен для получения нового Refresh токена через старый Refresh,
без необходимости заново логиниться.

TokenAccessAPI нужен для получения нового Access токена через Refresh токен,
без необходимости заново логиниться.
"""
from .views import TokenRefreshAPIView, TokenAccessAPIView

__all__ = ['TokenRefreshAPIView', 'TokenAccessAPIView']