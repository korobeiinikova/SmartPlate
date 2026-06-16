"""Модели рецептов, справочников и пользовательских действий."""

from django.conf import settings
from django.db import models
from django.urls import reverse


# ---------------------------------------------------------------------------
# Справочники
# ---------------------------------------------------------------------------

class CategoryEnum(models.TextChoices):
    """Допустимые названия категорий рецептов."""

    BREAKFAST = 'завтрак', 'завтрак'
    LUNCH = 'ужин', 'ужин'
    DINNER = 'обед', 'обед'
    DESSERTS = 'десерты', 'десерты'


class Tag(models.Model):
    """Тег для дополнительной группировки рецептов."""

    name = models.CharField(
        max_length=100,
        db_index=True,
        verbose_name='Название тега',
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        db_index=True,
        verbose_name='URL',
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('Recipes:tag', args=[self.slug])


class Product(models.Model):
    """Продукт, который может использоваться в составе рецепта."""

    name = models.CharField(max_length=50, verbose_name='Название продукта')
    unit = models.CharField(max_length=10, verbose_name='Единица измерения')
    avg_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Средняя цена',
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        db_index=True,
        verbose_name='URL',
    )

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return f'{self.name} {self.unit}'


class RecipeCategory(models.Model):
    """Основная категория рецепта: завтрак, обед, ужин или десерт."""

    name = models.CharField(
        max_length=100,
        choices=CategoryEnum.choices,
        verbose_name='Название категории',
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        db_index=True,
        verbose_name='URL',
    )

    class Meta:
        verbose_name = 'Категория рецепта'
        verbose_name_plural = 'Категории рецептов'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('Recipes:category', args=[self.slug])


# ---------------------------------------------------------------------------
# Рецепт и связанные с ним данные
# ---------------------------------------------------------------------------

class PublishedRecipeManager(models.Manager):
    """Менеджер, возвращающий только опубликованные рецепты."""

    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)


class Recipe(models.Model):
    """Основная публикация с описанием блюда и пищевой ценностью."""

    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=255, verbose_name='Название рецепта')
    description = models.TextField(blank=True, verbose_name='Описание')
    instructions = models.TextField(
        blank=True,
        verbose_name='Инструкция приготовления',
    )
    time_create = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время создания',
    )
    time_update = models.DateTimeField(
        auto_now=True,
        verbose_name='Время изменения',
    )
    is_published = models.BooleanField(
        choices=tuple((bool(value), label) for value, label in Status.choices),
        default=bool(Status.DRAFT),
        verbose_name='Статус',
    )
    category = models.ForeignKey(
        RecipeCategory,
        on_delete=models.PROTECT,
        related_name='recipes',
        verbose_name='Категория',
    )
    calories = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Калории (ккал)',
    )
    proteins = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Белки (г)',
    )
    fats = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Жиры (г)',
    )
    carbs = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Углеводы (г)',
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        db_index=True,
        verbose_name='URL',
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='recipes',
        verbose_name='Теги',
    )
    photo = models.ImageField(
        upload_to='recipes_photos/%Y/%m/%d/',
        blank=True,
        null=True,
        verbose_name='Изображение рецепта',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='recipes',
        null=True,
        blank=True,
        verbose_name='Автор',
    )

    objects = models.Manager()
    published = PublishedRecipeManager()

    class Meta:
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create']),
        ]
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            'Recipes:recipe_detail',
            kwargs={'recipe_slug': self.slug},
        )


class RecipeIngredient(models.Model):
    """Связывает рецепт с продуктом и хранит нужное количество."""

    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Количество',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients',
        verbose_name='Рецепт',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='used_in_recipes',
        verbose_name='Продукт',
    )

    class Meta:
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецептов'

    def __str__(self):
        return f'{self.quantity} {self.product.unit} {self.product.name}'


class RecipeDetail(models.Model):
    """Необязательные дополнительные сведения о рецепте."""

    recipe = models.OneToOneField(
        Recipe,
        on_delete=models.CASCADE,
        related_name='extra',
        verbose_name='Рецепт',
    )
    video_url = models.URLField(
        blank=True,
        verbose_name='Ссылка на видео',
    )
    cooking_tip = models.TextField(
        blank=True,
        verbose_name='Совет по приготовлению',
    )
    servings = models.PositiveSmallIntegerField(
        default=1,
        verbose_name='Порций',
    )

    class Meta:
        verbose_name = 'Деталь рецепта'
        verbose_name_plural = 'Детали рецептов'

    def __str__(self):
        return f'Детали для {self.recipe.title} на {self.servings} порций'


# ---------------------------------------------------------------------------
# Действия пользователей
# ---------------------------------------------------------------------------

class RecipeComment(models.Model):
    """Комментарий авторизованного пользователя к рецепту."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Рецепт',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='recipe_comments',
        verbose_name='Автор',
    )
    text = models.TextField(max_length=1000, verbose_name='Комментарий')
    time_create = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время создания',
    )

    class Meta:
        ordering = ['time_create']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'{self.author}: {self.text[:50]}'


class Favorite(models.Model):
    """Запись о добавлении рецепта пользователем в избранное."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт',
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='favorite_recipes',
        verbose_name='Пользователь',
    )
    time_create = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время добавления',
    )

    class Meta:
        ordering = ['-time_create']
        constraints = [
            # Один пользователь не может сохранить один рецепт дважды.
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique_favorite_recipe_per_user',
            ),
        ]
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'

    def __str__(self):
        return f'{self.user}: {self.recipe}'
