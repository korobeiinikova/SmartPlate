"""Представления каталога рецептов и пользовательских действий."""

import os
import uuid

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import AddRecipeModelForm, RecipeCommentForm, UploadFileForm
from .models import Favorite, Recipe, RecipeCategory, Tag
from .utils import DataMixin


# ---------------------------------------------------------------------------
# Информационные страницы и списки рецептов
# ---------------------------------------------------------------------------

def page_not_found(request, _exception):
    """Возвращает простую страницу для неизвестного URL."""
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


@login_required
def about(request):
    """Показывает информацию о сайте и последние рецепты."""
    paginator = Paginator(Recipe.published.all(), 3)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'about.html', {
        'page_obj': page_obj,
        'title': 'О сайте',
    })


class RecipesHome(DataMixin, ListView):
    """Главная страница со списком опубликованных рецептов."""
    template_name = 'home.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        return Recipe.published.select_related('category', 'author')

    def get_context_data(self, **kwargs):
        return self.get_mixin_context(
            super().get_context_data(**kwargs),
            title='Главная страница',
            cat_selected=0,
        )


class RecipesCategory(DataMixin, ListView):
    """Список опубликованных рецептов выбранной категории."""
    template_name = 'home.html'
    context_object_name = 'posts'
    allow_empty = True

    def get_queryset(self):
        return Recipe.published.filter(
            category__slug=self.kwargs['cat_slug'],
        ).select_related('category', 'author')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(RecipeCategory, slug=self.kwargs['cat_slug'])
        return self.get_mixin_context(
            context,
            title=f'Категория: {category.name}',
            cat_selected=category.pk,
        )


def show_tag_postlist(request, tag_slug):
    """Фильтрует опубликованные рецепты по выбранному тегу."""
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = tag.recipes.filter(
        is_published=Recipe.Status.PUBLISHED,
    ).select_related('category', 'author')
    return render(request, 'home.html', {
        'title': f'Тег: {tag.name}',
        'posts': posts,
        'tag_selected': tag,
    })


class RecipeDetail(DataMixin, DetailView):
    """Детальная страница опубликованного рецепта."""
    model = Recipe
    template_name = 'recipe_detail.html'
    slug_url_kwarg = 'recipe_slug'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        return get_object_or_404(
            Recipe.published.select_related('category', 'author'),
            slug=self.kwargs[self.slug_url_kwarg],
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = context['post']
        context['comment_form'] = RecipeCommentForm()
        context['comments'] = post.comments.select_related('author')
        context['favorites_count'] = post.favorites.count()
        context['is_favorite'] = (
            self.request.user.is_authenticated
            and post.favorites.filter(user=self.request.user).exists()
        )
        return self.get_mixin_context(context, title=post.title)


def recipes_by_portions(request, count):
    """Демонстрационная страница для выбранного количества порций."""
    return render(request, 'portion.html', {
        'title': f'Рецепты на {count} порций',
        'count': count,
    })


# ---------------------------------------------------------------------------
# Создание и загрузка файлов
# ---------------------------------------------------------------------------

class AddPageCreateView(LoginRequiredMixin, CreateView):
    """Создаёт рецепт и автоматически назначает текущего пользователя автором."""
    form_class = AddRecipeModelForm
    template_name = 'addpage.html'
    success_url = reverse_lazy('Recipes:home')
    extra_context = {'title': 'Добавление рецепта'}

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


@login_required
def add_recipe_model(request):
    """Альтернативный пример создания рецепта через связанную ModelForm."""
    if request.method == 'POST':
        form = AddRecipeModelForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            form.save_m2m()
            return redirect('Recipes:home')
    else:
        form = AddRecipeModelForm()
    return render(request, 'add_recipe_model.html', {
        'title': 'Добавление рецепта',
        'form': form,
    })


def handle_uploaded_file(uploaded_file):
    """Сохраняет файл под уникальным именем и возвращает это имя."""
    extension = os.path.splitext(uploaded_file.name)[1]
    unique_name = f'{uuid.uuid4().hex}{extension}'
    upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, unique_name)
    with open(file_path, 'wb+') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)
    return unique_name


def upload_file(request):
    """Обрабатывает отдельную демонстрационную форму загрузки файла."""
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            filename = handle_uploaded_file(request.FILES['file'])
            return render(request, 'upload_success.html', {'filename': filename})
    else:
        form = UploadFileForm()
    return render(request, 'upload_file.html', {'form': form})


# ---------------------------------------------------------------------------
# Управление рецептом и проверка владельца
# ---------------------------------------------------------------------------

class RecipeOwnerRequiredMixin(UserPassesTestMixin):
    """Разрешает изменение рецепта только его автору или администратору."""
    def test_func(self):
        recipe = self.get_object()
        return self.request.user.is_staff or recipe.author_id == self.request.user.id

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied
        return super().handle_no_permission()


class UpdatePage(LoginRequiredMixin, RecipeOwnerRequiredMixin, UpdateView):
    """Редактирование существующего рецепта."""
    model = Recipe
    fields = [
        'title', 'slug', 'description', 'instructions', 'is_published',
        'calories', 'proteins', 'fats', 'carbs', 'category', 'photo',
    ]
    template_name = 'addpage.html'
    success_url = reverse_lazy('Recipes:home')
    extra_context = {'title': 'Редактирование рецепта'}


class DeleteRecipe(LoginRequiredMixin, RecipeOwnerRequiredMixin, DeleteView):
    """Удаление рецепта после подтверждения."""
    model = Recipe
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('Recipes:home')


# ---------------------------------------------------------------------------
# Действия на странице рецепта
# ---------------------------------------------------------------------------

@require_POST
@login_required
def add_comment(request, recipe_slug):
    """Добавляет комментарий от имени текущего пользователя."""
    recipe = get_object_or_404(Recipe.published, slug=recipe_slug)
    form = RecipeCommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.recipe = recipe
        comment.author = request.user
        comment.save()
    return redirect(f'{recipe.get_absolute_url()}#comments')


@require_POST
@login_required
def toggle_favorite(request, recipe_slug):
    """Добавляет рецепт в избранное или удаляет его повторным нажатием."""
    recipe = get_object_or_404(Recipe.published, slug=recipe_slug)
    favorite = Favorite.objects.filter(recipe=recipe, user=request.user).first()
    if favorite:
        favorite.delete()
    else:
        Favorite.objects.create(recipe=recipe, user=request.user)
    return redirect(f'{recipe.get_absolute_url()}#favorite')
