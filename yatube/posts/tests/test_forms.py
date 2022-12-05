from django.test import TestCase, Client
from django.test import TestCase
from django.urls import reverse

from ..models import Group, Post, User


class FormsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title='Тестовый заголовок',
            description='Тестовое описание',
            slug='group-slug'
        )
        cls.anotherGroup = Group.objects.create(
            title='Другой тестовый заголовок',
            description='Другое тестовое описание',
            slug='another-group-slug'
        )
        cls.author = User.objects.create(username='Author')
        cls.not_author = User.objects.create(username='NotAuthor')
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=FormsTest.author,
            group=FormsTest.group
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.not_author = Client()
        self.authorized_client.force_login(FormsTest.author)
        self.not_author.force_login(FormsTest.not_author)

    def test_create_post_form(self):
        before_creating = Post.objects.count()
        form_data = {
            'text': 'Текст для нового поста',
            'group': FormsTest.group.id
        }
        response = (self.authorized_client.post(reverse(
            'posts:post_create'), data=form_data, follow=True))
        after_creating = Post.objects.count()
        self.assertEqual(before_creating + 1, after_creating)
        self.assertEqual(response.status_code, 200)

    def test_edit_post_form(self):
        form_data = {
            'text': 'Текст для измененного поста',
            'group': FormsTest.anotherGroup.id
        }
        (self.authorized_client.post(
            reverse('posts:post_edit', args=[FormsTest.post.id]),
            data=form_data, follow=True))
        edited_post = Post.objects.get(id='1')
        self.assertEqual(edited_post.text, 'Текст для измененного поста')
        self.assertEqual(edited_post.group, FormsTest.anotherGroup)
