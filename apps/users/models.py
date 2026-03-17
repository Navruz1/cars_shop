from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser

from .managers import UserManager, VerifyOTPManager, RefreshTokenModelManager


# Create your models here.

class User(AbstractUser):
    class RoleChoice(models.TextChoices):
        BUYER = 'buyer', _('Buyer')
        SELLER = 'seller', _('Seller')

    USERNAME_FIELD = 'phone_number'
    # REQUIRED_FIELDS = ['username']

    phone_number = models.CharField(max_length=13, unique=True, verbose_name=_("Phone Number"))
    role = models.CharField(max_length=10, choices=RoleChoice.choices, default=RoleChoice.BUYER, verbose_name=_("User Role"))
    is_active = models.BooleanField(default=False, verbose_name=_("Account is Active"))

    objects = UserManager()

    def __str__(self):
        return f"{self.username} ({self.phone_number})"


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

    objects = models.Manager()

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

    objects = RefreshTokenModelManager()

    def expired(self) -> bool:
        return self.expires_at <= timezone.now()


# One-Time Passwords

class Verify(models.Model):
    class Meta:
        abstract = True

    class Type(models.TextChoices):
        """Первые значения полей должны строго совпадать с названиями полей дочерних классов"""
        PHONE = 'phone_number', _('Phone number')
        EMAIL = 'email', _('Email')

    code = models.CharField(max_length=settings.OTP_INPUT_LENGTH)
    # data = models.CharField(max_length=100)  # +998561611611, user@mail.com, ...
    # verify_type = models.CharField(choices=Type.choices, default=Type.PHONE)  # phone_number, email, ...
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    objects = VerifyOTPManager()

    def expired(self) -> bool:
        return self.expires_at <= timezone.now()


# Phone Number Verify

class PhoneVerify(Verify):
    phone_number = models.CharField(max_length=13, verbose_name=_("Phone Number"))


# Email Verify

class EmailVerify(Verify):
    user_id = models.IntegerField()
    email = models.EmailField(max_length=100, verbose_name=_("E-Mail"))
    # verify_type = models.CharField(choices=Verify.Type.choices, default=Verify.Type.EMAIL)

# class VerifyOTP(models.Model):
#     class PurposeChoices(models.TextChoices):
#         REGISTER = 'register', _('Registration')
#         REVERIFY = 'reverify', _('Reverification')
#         PASSWORD_CHANGE = 'password_change', _('Change Password')
#
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     code = models.CharField(max_length=8)
#     purpose = models.CharField(
#         max_length=20,
#         choices=PurposeChoices.choices,
#         verbose_name=_('Purpose of Verify')
#     )
#     expires_at = models.DateTimeField()
#     is_used = models.BooleanField(default=False)
#
#     def not_expired(self) -> bool:
#         return self.expires_at >= timezone.now()
