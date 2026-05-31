from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User

class User(AbstractUser):
    photo = models.ImageField(
        upload_to='users/%Y/%m/%d/',
        blank=True,
        null=True,
        verbose_name='Фотография'
    )
    date_birth = models.DateField(
        blank=True,
        null=True,
        verbose_name='Дата рождения'
    )


class UserProxy(User):
    class Meta:
        proxy = True
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        permissions = [
            ('social_auth', 'Social Auth'),
        ]
