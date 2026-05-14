from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseNotFound, Http404
from .models import Recipe, RecipeCategory, Tag
from .forms import AddRecipeForm, AddRecipeModelForm, UploadFileForm
import uuid
import os
from django.conf import settings

def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


def index(request):
    posts = Recipe.published.all()
    data = {
        'title': 'Главная страница рецептов',
        'posts': posts,
        'cat_selected': 0,
    }
    return render(request, 'home.html', context=data)


def show_category(request, cat_slug):
    category = get_object_or_404(RecipeCategory, slug=cat_slug)
    posts = category.recipes.filter(is_published=Recipe.Status.PUBLISHED)
    data = {
        'title': f'Категория: {category.name}',
        'posts': posts,
        'cat_selected': category.pk,
    }
    return render(request, 'home.html', context=data)


def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = tag.recipes.filter(is_published=Recipe.Status.PUBLISHED)
    data = {
        'title': f'Тег: {tag.name}',
        'posts': posts,
        'tag_selected': tag,
    }
    return render(request, 'home.html', context=data)


def recipe_detail(request, recipe_slug):
    post = get_object_or_404(Recipe, slug=recipe_slug)
    data = {
        'title': post.title,
        'post': post,
    }
    return render(request, 'recipe_detail.html', context=data)


def recipes_by_portions(request, count):
    data = {
        'title': f'Рецепты на {count} порции',
        'count': count,
    }
    return render(request, 'portion.html', context=data)


def addpage(request):
    if request.method == 'POST':
        form = AddRecipeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data.copy()
            tags = data.pop('tags')
            try:
                new_recipe = Recipe.objects.create(**data)
                new_recipe.tags.set(tags)
                return redirect('Recipes:home')
            except Exception as e:
                form.add_error(None, f'Ошибка добавления рецепта: {e}')
    else:
        form = AddRecipeForm()

    return render(request, 'addpage.html', {
        'title': 'Добавление рецепта',
        'form': form,
        'cat_selected': 0,
    })


def add_recipe_model(request):
    if request.method == 'POST':
        form = AddRecipeModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('Recipes:home')
    else:
        form = AddRecipeModelForm()
    return render(request, 'add_recipe_model.html', {
        'title': 'Добавление рецепта (связанная форма)',
        'form': form,
    })



def handle_uploaded_file(f):
    ext = os.path.splitext(f.name)[1]
    unique_name = f"{uuid.uuid4().hex}{ext}"
    upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, unique_name)
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return unique_name


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            filename = handle_uploaded_file(request.FILES['file'])
            return render(request, 'upload_success.html', {'filename': filename})
    else:
        form = UploadFileForm()
    return render(request, 'upload_file.html', {'form': form})
