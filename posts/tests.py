from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Post, Category
from . import services
import services.common as services_common


User = get_user_model()


class CategoryModelTests(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            title='test category', title_ru='тестовая категория'
        )

    def test_model_fields(self):
        self.assertEqual(self.category.title, 'test category')
        self.assertEqual(self.category.title_ru, 'тестовая категория')

    def test_model_str(self):
        self.assertEqual(str(self.category), self.category.title)

    def test_model_get_absolute_url(self):
        url = reverse('category_posts', args=[self.category.pk])
        self.assertEqual(url, self.category.get_absolute_url())


class PostModelTests(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            title='test category', title_ru='тестовая категория'
        )
        self.user = User.objects.create_superuser(
            username='testuser', password='testpass'
        )
        self.post = Post.objects.create(
            title='test title', title_ru='тестовый заголовок',
            author=self.user, category=self.category,
            body='test body', body_ru='тестовое тело'
        )

    def test_model_fields(self):
        self.assertEqual(self.post.title, 'test title')
        self.assertEqual(self.post.title_ru, 'тестовый заголовок')
        self.assertEqual(self.post.author, self.user)
        self.assertEqual(self.post.category, self.category)
        self.assertEqual(self.post.body, 'test body')
        self.assertEqual(self.post.body_ru, 'тестовое тело')

    def test_model_str(self):
        self.assertEqual(str(self.post), self.post.title)

    def test_model_get_absolute_url(self):
        url = reverse('concrete_post', args=[self.post.pk])
        self.assertEqual(url, self.post.get_absolute_url())


class PostServicesTests(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            title='test category', title_ru='тестовая категория'
        )
        self.user = User.objects.create_superuser(
            username='testuser', password='testpass'
        )
        self.post = Post.objects.create(
            title='test title', title_ru='тестовый заголовок',
            author=self.user, category=self.category,
            body='test body', body_ru='тестовое тело'
        )

    def test_get_all_model_entries(self):
        all_posts = services_common.get_all_model_entries(Post)
        self.assertEqual(len(all_posts), 1)
        self.assertEqual(all_posts[0], self.post)

    def test_get_concrete_model_entry_by_pk(self):
        post = services_common.get_concrete_model_entry_by_pk(
            Post, self.post.pk
        )
        self.assertEqual(post, self.post)

    def test_search_posts(self):
        posts = services.search_posts('test')
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0], self.post)

    def test_get_category_posts(self):
        category, posts = services.get_category_posts(self.category.pk)
        self.assertEqual(category, self.category)
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0], self.post)


class PostViewsTests(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            title='test category', title_ru='тестовая категория'
        )
        self.user = User.objects.create_superuser(
            username='testuser', password='testpass'
        )
        self.client.login(username='testuser', password='testpass')
        self.post = Post.objects.create(
            title='test title', title_ru='тестовый заголовок',
            author=self.user, category=self.category,
            body='test body', body_ru='тестовое тело'
        )

    def test_all_posts(self):
        response = self.client.get(reverse('all_posts'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/all_posts.html')
        self.assertContains(response, self.post.title)

    def test_concrete_post(self):
        response = self.client.get(
            reverse('concrete_post', args=[self.post.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/concrete_post.html')
        self.assertContains(response, self.post.title)

    def test_change_post(self):
        response = self.client.get(
            reverse('change_post', args=[self.post.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/change.html')
        self.assertContains(response, self.post.title)

    def test_delete_post(self):
        response = self.client.get(
            reverse('delete_post', args=[self.post.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/delete.html')
        self.assertContains(response, self.post.title)

    def test_category_posts(self):
        response = self.client.get(
            reverse('category_posts', args=[self.category.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/category_posts.html')
        self.assertContains(response, self.category.title)
        self.assertContains(response, self.post.title)

    def test_search_post(self):
        response = self.client.get(
            reverse('search_posts') + f"?query={self.post.title}"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/search_posts.html')
        self.assertContains(response, self.post.title)

    def test_create_post(self):
        response = self.client.get(reverse('create_post'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/create.html')
        self.assertContains(response, 'Create a new post')
