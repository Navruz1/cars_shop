from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .helpers import PHONE_REGEX


# Create your models here.

class User(AbstractUser):
    class RoleChoice(models.TextChoices):
        BUYER = 'buyer', _('Buyer')
        SELLER = 'seller', _('Seller')

    phone_number = models.CharField(
        max_length=13,
        unique=True,
        validators=[PHONE_REGEX],
        verbose_name=_("Phone number"))

    role = models.CharField(
        max_length=10,
        choices=RoleChoice.choices,
        default=RoleChoice.BUYER,
        verbose_name=_("User role"))

    def __str__(self):
        return f"{self.username}"


# Refresh Token

class RefreshToken(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='refresh_tokens'
    )
    token = models.TextField(unique=True)
    is_valid = models.BooleanField(default=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)

    replaced_by_token = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='replaced_tokens'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# For User Account Actions

class AuthLog(models.Model):
    class ActionChoices(models.TextChoices):
        LOGIN = 'login', _('Login')
        LOGOUT = 'logout', _('Logout')
        REGISTER = 'register', _('Register')
        REFRESH = 'refresh', _('Refresh')
        PASSWORD_CHANGE = 'password_change', _('Change Password')

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='auth_logs',
        verbose_name=_('User'),
    )
    action = models.CharField(
        max_length=20,
        choices=ActionChoices.choices,
        verbose_name=_('Action'),
    )
    ip_address = models.GenericIPAddressField(
        verbose_name=_('IP Address'),
        null=True,
        blank=True,
    )
    user_agent = models.TextField(
        verbose_name=_('User Agent'),
        blank=True,
    )
    metadata = models.JSONField(
        default=dict,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)





