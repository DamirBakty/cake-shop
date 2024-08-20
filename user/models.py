from django.contrib.auth.models import AbstractUser
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    """Модель пользователя."""
    name = models.CharField(
        verbose_name='Имя',
        max_length=200,
        help_text='Введите имя',
        blank=False,
    )
    phone = PhoneNumberField(
        verbose_name='телефон',
        region='RU',
        blank=False,
        null=False,
        unique=True,
    )
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        help_text='Введите адрес электронной почты',
        blank=True,
        unique=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
