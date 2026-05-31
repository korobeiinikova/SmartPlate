from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseNotFound
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView
from .models import Recipe, RecipeCategory, Tag
from .forms import AddRecipeModelForm, UploadFileForm
import uuid
import os
from django.conf import settings
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from .utils import DataMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin



def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


@login_required
def about(request):
    recipes_list = Recipe.published.all()
    paginator = Paginator(recipes_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'about.html', {
        'page_obj': page_obj,
        'title': 'О сайте'
    })


class RecipesHome(DataMixin, ListView):
    template_name = 'home.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        return Recipe.published.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        return self.get_mixin_context(super().get_context_data(**kwargs),
                                      title='Главная страница',
                                      cat_selected=0)


class RecipesCategory(DataMixin, ListView):
    template_name = 'home.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Recipe.published.filter(category__slug=self.kwargs['cat_slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = get_object_or_404(RecipeCategory, slug=self.kwargs['cat_slug'])
        return self.get_mixin_context(context,
                                      title=f'Категория: {cat.name}',
                                      cat_selected=cat.pk)


def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = tag.recipes.filter(is_published=Recipe.Status.PUBLISHED)
    data = {
        'title': f'Тег: {tag.name}',
        'posts': posts,
        'tag_selected': tag,
    }
    return render(request, 'home.html', context=data)


class RecipeDetail(DataMixin, DetailView):
    model = Recipe
    template_name = 'recipe_detail.html'
    slug_url_kwarg = 'recipe_slug'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        return get_object_or_404(Recipe.published, slug=self.kwargs[self.slug_url_kwarg])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title)


def recipes_by_portions(request, count):
    data = {
        'title': f'Рецепты на {count} порции',
        'count': count,
    }
    return render(request, 'portion.html', context=data)


class AddPageCreateView(LoginRequiredMixin, CreateView):
    form_class = AddRecipeModelForm
    template_name = 'addpage.html'
    success_url = reverse_lazy('Recipes:home')
    extra_context = {'title': 'Добавление рецепта'}

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


@login_required
def add_recipe_model(request):
    if request.method == 'POST':
        form = AddRecipeModelForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            if request.user.is_authenticated:
                recipe.author = request.user
            recipe.save()
            form.save_m2m()
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


class UpdatePage(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = 'Recipes.change_recipe'
    model = Recipe
    fields = ['title', 'slug', 'description', 'instructions', 'is_published',
              'calories', 'proteins', 'fats', 'carbs', 'category', 'photo']
    template_name = 'addpage.html'
    success_url = reverse_lazy('Recipes:home')
    extra_context = {'title': 'Редактирование рецепта'}


class DeleteRecipe(LoginRequiredMixin, DeleteView):
    model = Recipe
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('Recipes:home')
