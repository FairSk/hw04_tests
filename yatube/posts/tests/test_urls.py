# posts/tests/test_urls.py
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post

User = get_user_model()


class StaticURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_homepage(self):
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
        )

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        group = PostModelTest.group
        post = PostModelTest.post
        self.assertEqual(group.title, 'Тестовая группа')
        self.assertEqual(post.text, 'Тестовый пост')


class TaskURLTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='HasNoName')
        cls.non_posts = User.objects.create_user(username='NoPosts')
        Group.objects.create(
            title='Тестовый заголовок',
            description='Тестовое описание',
            slug='group-slug'
        )
        Post.objects.create(
            author=cls.user,
            text='test-text'
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.non_posts_user = Client()
        self.non_posts_user.force_login(self.non_posts)

    def test_main_page_for_everyone(self):
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200,
                         'Main page isn\'t available')

    def test_group_for_everyone(self):
        response = self.guest_client.get('/group/group-slug/')
        self.assertEqual(response.status_code, 200,
                         'Group page isn\'t available')

    def test_profile_for_everyone(self):
        response = self.guest_client.get('/profile/HasNoName/')
        self.assertEqual(response.status_code, 200,
                         'Profile page isn\'t available')

    def test_create_for_logged(self):
        response = self.authorized_client.get('/create/')
        self.assertEqual(response.status_code, 200,
                         'Create page isn\'t available')

    def test_create_for_unlogged(self):
        response = self.guest_client.get('/create/', follow=True)
        self.assertRedirects(response, '/auth/login/?next=/create/')

    def test_posts_for_everyone(self):
        response = self.guest_client.get('/posts/1/')
        self.assertEqual(response.status_code, 200,
                         'Posts page isn\'t available')

    def test_posts_edit_for_author(self):
        response = self.non_posts_user.get('/posts/1/')
        self.assertEqual(response.status_code, 200,
                         'Posts Edit page isn\'t available')

    def test_posts_edit_for_not_author(self):
        response = self.non_posts_user.get('/posts/1/edit/')
        self.assertRedirects(response, '/posts/1/')

    def test_posts_edit_for_unlogged(self):
        response = self.guest_client.get('/posts/1/edit/', follow=True)
        self.assertRedirects(response, '/auth/login/?next=/posts/1/edit/')

    def test_for_404_page(self):
        response = self.authorized_client.get('/123/')
        self.assertEqual(response.status_code, 404,
                         'Unavailable page is available???')
