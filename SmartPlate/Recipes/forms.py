from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from .models import RecipeCategory, Tag, Recipe


class RussianValidator:
    ALLOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщьыъэюя0123456789- "

    def __init__(self, message=None):
        self.message = message if message else "Должны быть только русские символы, дефис и пробел."

    def __call__(self, value):
        if not (set(value) <= set(self.ALLOWED_CHARS)):
            raise ValidationError(self.message)


class AddRecipeForm(forms.Form):
    title = forms.CharField(
        max_length=255, min_length=5,
        label="Название рецепта",
        widget=forms.TextInput(attrs={'class': 'form-input'}),
        validators=[RussianValidator()],
        error_messages={
            'min_length': 'Слишком короткое название (минимум 5 символов)',
            'required': 'Название обязательно'
        }
    )
    slug = forms.SlugField(
        max_length=255, label="URL (slug)",
        validators=[
            MinLengthValidator(5, message="Минимум 5 символов"),
            MaxLengthValidator(100, message="Максимум 100 символов"),
        ]
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'cols': 50, 'rows': 5}),
        required=False, label="Краткое описание"
    )
    instructions = forms.CharField(
        widget=forms.Textarea(attrs={'cols': 50, 'rows': 10}),
        required=False, label="Подробный рецепт"
    )
    is_published = forms.BooleanField(
        required=False, initial=True, label="Опубликовано"
    )
    category = forms.ModelChoiceField(
        queryset=RecipeCategory.objects.all(),
        empty_label="Категория не выбрана",
        label="Категория"
    )
    calories = forms.DecimalField(max_digits=10, decimal_places=2, label="Калории (ккал)")
    proteins = forms.DecimalField(max_digits=10, decimal_places=2, label="Белки (г)")
    fats = forms.DecimalField(max_digits=10, decimal_places=2, label="Жиры (г)")
    carbs = forms.DecimalField(max_digits=10, decimal_places=2, label="Углеводы (г)")
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False, label="Теги"
    )

    # Пользовательская валидация для заголовка (длина)
    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 100:
            raise ValidationError("Длина названия превышает 100 символов")
        return title


class AddRecipeModelForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=RecipeCategory.objects.all(),
        empty_label="Категория не выбрана",
        label="Категории"
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        label="Теги"
    )

    class Meta:
        model = Recipe
        fields = ['title', 'slug', 'description', 'instructions',
                  'is_published', 'calories', 'proteins', 'fats', 'carbs',
                  'category', 'tags', 'photo']
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
            'description': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
            'instructions': forms.Textarea(attrs={'cols': 50, 'rows': 10}),
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-file'}),
        }
        error_messages = {
            'title': {
                'required': 'Название обязательно',
            },
            'slug': {
                'unique': 'Рецепт с таким URL уже существует',
            }
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 100:
            raise ValidationError('Длина названия превышает 100 символов')
        return title


class UploadFileForm(forms.Form):
    file = forms.ImageField(label="Изображение")