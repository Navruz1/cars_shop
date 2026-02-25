from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime, timezone
from django.utils.translation import gettext_lazy as _
from .helpers import PHONE_REGEX

# Create your models here.
class User(AbstractUser):
    class RoleChoice(models.TextChoices):
        BUYER = 'buyer', _('Buyer')
        SELLER = 'seller', _('Seller')

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username']

    phone_number = models.CharField(max_length=13, unique=True, validators=[PHONE_REGEX], verbose_name=_("Phone number"))
    role = models.CharField(max_length=10, choices=RoleChoice.choices, default=RoleChoice.BUYER, verbose_name=_("User role"))

    def __str__(self):
        return f"{self.username} ({self.phone_number})"

    def generate_username_from_firstname(self):
        """Устанавливает username как first_name+id после сохранения."""
        if not self.id:
            raise ValueError("User must be saved before generating username.")
        self.username = f"{self.first_name[:20]}{self.id}"
        self.save(update_fields=['username'])
        return self.username


# For User Account Actions
class AuthLog(models.Model):
    class ActionChoices(models.TextChoices):
        LOGIN = 'login', _('Login')
        LOGOUT = 'logout', _('Logout')
        REGISTER = 'register', _('Register')
        REFRESH = 'refresh', _('Refresh')
        PASSWORD_CHANGE = 'password_change', _('Change Password')

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auth_logs', verbose_name=_('User'))
    action = models.CharField(max_length=20, choices=ActionChoices.choices, verbose_name=_('Action'))
    ip_address = models.GenericIPAddressField(verbose_name=_('IP Address'), null=True, blank=True)
    user_agent = models.TextField(verbose_name=_('User Agent'), blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=['user', 'created_at'])]


# Refresh Token
class RefreshTokenModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='refresh_tokens')
    token = models.TextField(unique=True)
    is_valid = models.BooleanField(default=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    replaced_by_token = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='replaced_tokens')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def generate_for_user(cls, user, *, ip_address=None, user_agent=""):
        from rest_framework_simplejwt.tokens import RefreshToken

        refresh = RefreshToken.for_user(user)
        expires_at = datetime.fromtimestamp(refresh.payload.get('exp'), tz=timezone.utc)

        obj = cls.objects.create(
            user=user,
            token=str(refresh),
            ip_address=ip_address,
            user_agent=user_agent,
            is_valid=True,
            expires_at=expires_at
        )
        obj.access_token = str(refresh.access_token)
        return obj


