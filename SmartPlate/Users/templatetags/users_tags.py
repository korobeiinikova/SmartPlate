from django import template

register = template.Library()


menu = [
    {'title': 'Рецепты', 'url_name': 'Recipes:home'},
    {'title': 'О сайте', 'url_name': 'Recipes:about'},
    {'title': 'Пользователи', 'url_name': 'Users:home'},
]


@register.simple_tag()
def get_menu():
    return menu
