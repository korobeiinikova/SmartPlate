menu = [
    {'title': 'Рецепты', 'url_name': 'Recipes:home'},
    {'title': 'О сайте', 'url_name': 'Recipes:about'},
    {'title': 'Пользователь', 'url_name': 'Users:profile'},
]


def get_users_context(request):
    return {'mainmenu': menu}
