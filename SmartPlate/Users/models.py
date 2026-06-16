"""Пользовательская модель проекта."""

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Стандартный пользователь Django с фотографией и датой рождения."""

    photo = models.ImageField(
        upload_to='users/%Y/%m/%d/',
        blank=True,
        null=True,
        verbose_name='Фотография',
    )
    date_birth = models.DateField(
        blank=True,
        null=True,
        verbose_name='Дата рождения',
    )


class UserProxy(User):
    """Прокси-модель для дополнительных настроек пользователей в админке."""

    class Meta:
        proxy = True
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        permissions = [
            ('social_auth', 'Social Auth'),
        ]
