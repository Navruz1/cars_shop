from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


# Create your models here.

phone_regex = RegexValidator(
    regex=r'^\+998\d{9}$',
    message="Номер должен начинаться с +998 и содержать 9 цифр после него."
)

class User(AbstractUser):
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=13,
        unique=True
    )

    USER_ROLES = (
        ('buyer', 'Покупатель'),
        ('seller', 'Продавец'),
    )
    role = models.CharField(
        max_length=10,
        choices=USER_ROLES,
        default='buyer'
    )

    def __str__(self):
        return f"{self.username}"

