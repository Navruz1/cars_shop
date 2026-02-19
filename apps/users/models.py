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
        choices=RoleChoice,
        default='buyer',
        verbose_name=_("User role"))

    def __str__(self):
        return f"{self.username}"


# For User Account Actions

class AuthLog(models.Model):
    class ActionChoices(models.TextChoices):
        LOGIN = 'login', _('Login')
        LOGOUT = 'logout', _('Logout')
        REGISTER = 'register', _('Register')
        REFRESH = 'refresh', _('Refresh')
        PASSWORD_CHANGE = 'password_change', _('Change Password')

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('User'))
    action = models.CharField(max_length=20, choices=ActionChoices.choices, verbose_name=_('Action'))
    ip_address = models.GenericIPAddressField(verbose_name=_('IP Address'), null=True, blank=True)
    user_agent = models.TextField(verbose_name=_('User Agent'))
    metadata = models.JSONField(default=dict)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)





