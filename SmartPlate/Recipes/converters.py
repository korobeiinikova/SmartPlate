"""Пользовательские преобразователи параметров URL."""


class PositiveIntConverter:
    """Принимает в URL только целые числа больше нуля."""

    regex = r'[1-9][0-9]*'

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return str(value)
