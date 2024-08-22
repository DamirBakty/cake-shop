from django.contrib.auth.models import AbstractUser
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    """Модель пользователя."""
    phone = PhoneNumberField(
        verbose_name='телефон',
        region='RU',
        blank=False,
        null=False,
        unique=True,
    )
    address = models.CharField(
        verbose_name='Адрес',
        max_length=200,
        blank=False,
        null=False,
    )

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
