from django.test import TestCase
from django.urls import reverse

# Не понимаю почему это строка лишняя,
#  если мы ее удалим, то как я создам в дб объекты
from ..models import Group, Post, User


class RoutesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create(username='Author')
        cls.group = Group.objects.create(
            title='Тестовый заголовок',
            description='Тестовое описание',
            slug='group-slug'
        )
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=RoutesTests.author,
            group=RoutesTests.group
        )
        cls.PATHS = {
            reverse('posts:index'): '/',
            reverse('posts:post_create'): '/create/',
            reverse('posts:post_edit', args=[RoutesTests.post.id]):
                '/posts/1/edit/',
            reverse('posts:group_posts', args=[RoutesTests.group.slug]):
                '/group/group-slug/',
            reverse('posts:profile', args=[RoutesTests.author.username]):
                '/profile/Author/',
            reverse('posts:post_detail', args=[RoutesTests.post.id]):
                '/posts/1/'
        }

    def test__routes(self):
        for reversed_path, path in self.PATHS.items():
            self.assertEqual(reversed_path, path)
