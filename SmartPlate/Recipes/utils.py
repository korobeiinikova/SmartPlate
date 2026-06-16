"""Общие вспомогательные классы приложения рецептов."""


class DataMixin:
    """Добавляет стандартные данные в контекст страниц со списками рецептов."""

    paginate_by = 3

    def get_mixin_context(self, context, **kwargs):
        """Дополняет контекст заголовком и выбранной категорией."""
        context.setdefault('cat_selected', None)
        context.update(kwargs)
        return context
