"""Дополнительный способ входа пользователя по адресу электронной почты."""

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend


class EmailAuthBackend(BaseBackend):
    """Проверяет e-mail и пароль вместо стандартной пары логин-пароль."""

    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = get_user_model()

        try:
            user = user_model.objects.get(email=username)
        except user_model.DoesNotExist:
            return None

        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        """Восстанавливает пользователя по идентификатору из сессии."""
        user_model = get_user_model()

        try:
            return user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            return None
