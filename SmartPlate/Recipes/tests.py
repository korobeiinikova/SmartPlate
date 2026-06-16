"""Тесты создания рецептов, прав доступа и пользовательских действий."""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Favorite, Recipe, RecipeCategory, RecipeComment


class RecipeInteractionTests(TestCase):
    """Проверяет основные пользовательские сценарии приложения."""

    @classmethod
    def setUpTestData(cls):
        """Создаёт общие данные один раз для всех тестов класса."""
        user_model = get_user_model()
        cls.author = user_model.objects.create_user(
            username='author',
            password='test-password',
        )
        cls.other_user = user_model.objects.create_user(
            username='reader',
            password='test-password',
        )
        cls.category = RecipeCategory.objects.create(
            name=RecipeCategory._meta.get_field('name').choices[0][0],
            slug='test-category',
        )
        cls.recipe = Recipe.objects.create(
            title='Test recipe',
            description='Description',
            instructions='Instructions',
            is_published=True,
            category=cls.category,
            calories=100,
            proteins=10,
            fats=5,
            carbs=20,
            slug='test-recipe',
            author=cls.author,
        )

    # Создание контента.
    def test_recipe_creation_assigns_logged_in_user_as_author(self):
        self.client.force_login(self.other_user)

        response = self.client.post(reverse('Recipes:addpage'), {
            'title': 'User recipe',
            'slug': 'user-recipe',
            'description': 'Description',
            'instructions': 'Instructions',
            'is_published': 'True',
            'calories': '120',
            'proteins': '12',
            'fats': '6',
            'carbs': '18',
            'category': self.category.pk,
        })

        self.assertRedirects(response, reverse('Recipes:home'))
        self.assertEqual(
            Recipe.objects.get(slug='user-recipe').author,
            self.other_user,
        )

    # Проверка объектных прав.
    def test_only_author_or_staff_can_edit_recipe(self):
        edit_url = reverse('Recipes:edit_page', args=[self.recipe.pk])

        self.assertRedirects(
            self.client.get(edit_url),
            f'{reverse("Users:login")}?next={edit_url}',
        )

        self.client.force_login(self.other_user)
        self.assertEqual(self.client.get(edit_url).status_code, 403)

        self.client.force_login(self.author)
        self.assertEqual(self.client.get(edit_url).status_code, 200)

    def test_only_author_or_staff_can_delete_recipe(self):
        delete_url = reverse('Recipes:delete_recipe', args=[self.recipe.pk])

        self.client.force_login(self.other_user)
        self.assertEqual(self.client.get(delete_url).status_code, 403)

        self.client.force_login(self.author)
        self.assertEqual(self.client.get(delete_url).status_code, 200)

    # Комментарии.
    def test_authenticated_user_can_add_comment(self):
        self.client.force_login(self.other_user)

        response = self.client.post(
            reverse('Recipes:add_comment', args=[self.recipe.slug]),
            {'text': 'Useful recipe'},
        )

        self.assertRedirects(
            response,
            f'{self.recipe.get_absolute_url()}#comments',
        )
        comment = RecipeComment.objects.get()
        self.assertEqual(comment.recipe, self.recipe)
        self.assertEqual(comment.author, self.other_user)
        self.assertEqual(comment.text, 'Useful recipe')

    def test_anonymous_user_cannot_add_comment(self):
        response = self.client.post(
            reverse('Recipes:add_comment', args=[self.recipe.slug]),
            {'text': 'Anonymous comment'},
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(RecipeComment.objects.exists())

    # Избранное.
    def test_recipe_can_be_added_to_and_removed_from_favorites(self):
        self.client.force_login(self.other_user)
        favorite_url = reverse(
            'Recipes:toggle_favorite',
            args=[self.recipe.slug],
        )

        response = self.client.post(favorite_url)
        self.assertRedirects(
            response,
            f'{self.recipe.get_absolute_url()}#favorite',
        )
        self.assertTrue(
            Favorite.objects.filter(
                recipe=self.recipe,
                user=self.other_user,
            ).exists(),
        )

        self.client.post(favorite_url)
        self.assertFalse(Favorite.objects.exists())

    # Страницы профиля.
    def test_profile_and_favorites_are_separate_pages(self):
        Favorite.objects.create(recipe=self.recipe, user=self.other_user)
        own_recipe = Recipe.objects.create(
            title='Reader recipe',
            description='Description',
            instructions='Instructions',
            is_published=True,
            category=self.category,
            calories=100,
            proteins=10,
            fats=5,
            carbs=20,
            slug='reader-recipe',
            author=self.other_user,
        )
        self.client.force_login(self.other_user)

        response = self.client.get(reverse('Users:profile'))
        favorites_response = self.client.get(reverse('Users:favorites'))
        settings_response = self.client.get(reverse('Users:profile_settings'))

        self.assertIn(own_recipe, response.context['my_recipes'])
        self.assertNotContains(response, 'Test recipe')
        self.assertIn(
            self.recipe,
            favorites_response.context['favorite_recipes'],
        )
        self.assertEqual(settings_response.status_code, 200)

    # Пустые списки должны открываться без ошибки 404.
    def test_empty_category_page_is_available(self):
        empty_category = RecipeCategory.objects.create(
            name=RecipeCategory._meta.get_field('name').choices[1][0],
            slug='empty-category',
        )

        response = self.client.get(
            reverse('Recipes:category', args=[empty_category.slug]),
        )

        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context['posts'], [])
