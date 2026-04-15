from django.db import models
from django.urls import reverse


class CategoryEnum(models.TextChoices):
    BREAKFAST = 'завтрак', 'завтрак'
    LUNCH = 'ужин', 'ужин'
    DINNER = 'обед', 'обед'
    DESSERTS = 'десерты', 'десерты'


class Tag(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('Recipes:tag', args=[self.slug])


class Product(models.Model):
    name = models.CharField(max_length=50)
    unit = models.CharField(max_length=10)
    avg_price = models.DecimalField(max_digits=10, decimal_places=2)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return f"{self.name} {self.unit}"


class RecipeCategory(models.Model):
    name = models.CharField(max_length=100, choices=CategoryEnum.choices)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('Recipes:category', args=[self.slug])


class Recipe(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    instructions = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    is_published = models.BooleanField(choices=Status.choices, default=Status.DRAFT)
    category = models.ForeignKey(RecipeCategory, on_delete=models.PROTECT, related_name='recipes')
    calories = models.DecimalField(max_digits=10, decimal_places=2)
    proteins = models.DecimalField(max_digits=10, decimal_places=2)
    fats = models.DecimalField(max_digits=10, decimal_places=2)
    carbs = models.DecimalField(max_digits=10, decimal_places=2)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    tags = models.ManyToManyField('Tag', blank=True, related_name='recipes')

    class Meta:
        ordering = ['-time_create']
        indexes = [models.Index(fields=['-time_create']), ]
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('Recipes:recipe_detail', kwargs={'recipe_slug': self.slug})

    objects = models.Manager()

    class PublishedManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(is_published=Recipe.Status.PUBLISHED)

    published = PublishedManager()


class RecipeIngredient(models.Model):
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='used_in_recipes')

    def __str__(self):
        return f"{self.quantity} {self.product.unit} {self.product.name}"


class RecipeDetail(models.Model):
    recipe = models.OneToOneField('Recipe', on_delete=models.CASCADE, related_name='extra')
    video_url = models.URLField(blank=True, verbose_name="Ссылка на видео")
    cooking_tip = models.TextField(blank=True, verbose_name="Совет по приготовлению")
    servings = models.PositiveSmallIntegerField(default=1, verbose_name="Порций")

    def __str__(self):
        return f"Детали для {self.recipe.title} на {self.servings}: {self.cooking_tip}"
