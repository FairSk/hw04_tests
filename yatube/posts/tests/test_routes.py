from django.test import TestCase
from django.urls import reverse

from ..models import Group, Post, User


class RoutesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create(username='Author')
        cls.not_author = User.objects.create(username='NotAuthor')
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=RoutesTests.author
        )
        cls.group = Group.objects.create(
            title='Тестовый заголовок',
            description='Тестовое описание',
            slug='group-slug'
        )

    def setUp(self):
        self.index = reverse('posts:index')
        self.create = reverse('posts:post_create')
        self.edit = reverse('posts:post_edit', args=[self.post.id])
        self.group_post = reverse('posts:group_posts', args=[self.group.slug])
        self.profile = reverse('posts:profile', args=[self.author.username])
        self.detail = reverse('posts:post_detail', args=[self.post.id])

    def test_index_route(self):
        self.assertEqual(self.index, '/')
        self.assertEqual(self.create, '/create/')
        self.assertEqual(self.edit, '/posts/1/edit/')
        self.assertEqual(self.group_post, '/group/group-slug/')
        self.assertEqual(self.profile, '/profile/Author/')
        self.assertEqual(self.detail, '/posts/1/')
