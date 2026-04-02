from django.db import models
from django.urls import reverse


class CategoryEnum(models.TextChoices):
    BREAKFAST = 'завтрак', 'завтрак'
    LUNCH = 'ужин', 'ужин'
    DINNER = 'обед', 'обед'
    DESSERTS = 'десерты', 'десерты'


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
    calories = models.DecimalField(max_digits=10, decimal_places=2)
    proteins = models.DecimalField(max_digits=10, decimal_places=2)
    fats = models.DecimalField(max_digits=10, decimal_places=2)
    carbs = models.DecimalField(max_digits=10, decimal_places=2)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

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
