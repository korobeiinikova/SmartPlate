"""Глобальные данные, доступные во всех шаблонах сайта."""

MAIN_MENU = [
    {'title': 'Рецепты', 'url_name': 'Recipes:home'},
    {'title': 'О сайте', 'url_name': 'Recipes:about'},
]


def get_users_context(request):
    """Добавляет пункты главного меню в контекст каждого шаблона."""
    return {'mainmenu': MAIN_MENU}
