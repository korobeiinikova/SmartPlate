"""Формы создания рецептов, комментариев и загрузки изображений."""

from django import forms
from django.core.exceptions import ValidationError

from .models import Recipe, RecipeCategory, RecipeComment, Tag


class AddRecipeModelForm(forms.ModelForm):
    """Форма создания рецепта пользователем."""

    category = forms.ModelChoiceField(
        queryset=RecipeCategory.objects.all(),
        empty_label='Категория не выбрана',
        label='Категория',
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        label='Теги',
    )

    class Meta:
        model = Recipe
        fields = [
            'title',
            'slug',
            'description',
            'instructions',
            'is_published',
            'calories',
            'proteins',
            'fats',
            'carbs',
            'category',
            'tags',
            'photo',
        ]
        labels = {
            'title': 'Название рецепта',
            'slug': 'URL',
            'description': 'Краткое описание',
            'instructions': 'Подробный рецепт',
            'is_published': 'Опубликовано',
            'calories': 'Калории (ккал)',
            'proteins': 'Белки (г)',
            'fats': 'Жиры (г)',
            'carbs': 'Углеводы (г)',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'rows': 5}),
            'instructions': forms.Textarea(attrs={'rows': 10}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-file'}),
        }
        error_messages = {
            'title': {
                'required': 'Название обязательно',
            },
            'slug': {
                'unique': 'Рецепт с таким URL уже существует',
            },
        }

    def clean_title(self):
        """Не позволяет использовать слишком длинное название."""
        title = self.cleaned_data['title']
        if len(title) > 100:
            raise ValidationError(
                'Длина названия не должна превышать 100 символов',
            )
        return title


class RecipeCommentForm(forms.ModelForm):
    """Форма добавления комментария под рецептом."""

    class Meta:
        model = RecipeComment
        fields = ['text']
        labels = {'text': 'Комментарий'}
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 4,
                'maxlength': 1000,
                'placeholder': 'Напишите комментарий',
            }),
        }


class UploadFileForm(forms.Form):
    """Простая демонстрационная форма загрузки изображения."""

    file = forms.ImageField(label='Изображение')
