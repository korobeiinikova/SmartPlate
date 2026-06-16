"""Представления авторизации и личного кабинета."""

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from Recipes.models import Recipe

from .forms import LoginUserForm, ProfileUserForm, RegisterUserForm


def index(request):
    """Стартовая страница раздела пользователей."""
    return render(request, 'users/index.html')


class LoginUser(LoginView):
    """Авторизация по логину или e-mail."""
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}

    def get_success_url(self):
        return reverse_lazy('Recipes:home')


class RegisterUser(CreateView):
    """Регистрация нового пользователя."""
    form_class = RegisterUserForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('Users:login')
    extra_context = {'title': 'Регистрация'}


class ProfileUser(LoginRequiredMixin, TemplateView):
    """Главная страница профиля со списком авторских рецептов."""
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_recipes'] = self.request.user.recipes.select_related('category')
        return context


class FavoriteRecipes(LoginRequiredMixin, TemplateView):
    """Отдельная страница сохранённых пользователем рецептов."""
    template_name = 'users/favorites.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favorite_recipes'] = Recipe.objects.filter(
            favorites__user=self.request.user,
            is_published=True,
        ).select_related('category', 'author')
        return context


class ProfileSettings(LoginRequiredMixin, UpdateView):
    """Изменение фотографии и даты рождения текущего пользователя."""
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile_settings.html'
    success_url = reverse_lazy('Users:profile')

    def get_object(self, queryset=None):
        return self.request.user
