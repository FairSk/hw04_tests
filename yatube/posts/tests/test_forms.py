from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from ..models import Group, Post

User = get_user_model()


class TaskFormsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='HasNoName')
        Group.objects.create(
            title='Тестовый заголовок',
            description='Тестовое описание',
            slug='group-slug'
        )
        Post.objects.create(
            author=User.objects.get(username='HasNoName'),
            text='Текст',
            group=Group.objects.get(slug='group-slug')
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_post(self):
        tasks_count = Post.objects.count()
        form_data = {
            'text': 'Текст из формы'
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertEqual(Post.objects.count(), tasks_count + 1)
        self.assertEqual(response.status_code, 200)

    def test_edit_post(self):
        form_data = {
            'text': 'Новый текст из формы'
        }
        self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': '1'}),
            data=form_data,
            follow=True
        )
        edited_post = Post.objects.get(id='1')
        self.assertEqual(edited_post.text, 'Новый текст из формы')
