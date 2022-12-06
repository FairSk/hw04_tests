from django.test import TestCase
from django.urls import reverse

# Не понимаю почему это строка лишняя,
#  если мы ее удалим, то как я создам в дб объекты,
#   чтоб сделать к ним запросы
from ..models import Group, Post, User


author_user = User.objects.create(username='Author')
post = Post.objects.create(
    text='Тестовый текст',
    author=author_user)

group = Group.objects.create(
    title='Тестовый заголовок',
    description='Тестовое описание',
    slug='group-slug')

PATHS = {
    reverse('posts:index'): '/',
    reverse('posts:post_create'): '/create/',
    reverse('posts:post_edit', args=[post.id]): '/posts/1/edit/',
    reverse('posts:group_posts', args=[group.slug]): '/group/group-slug/',
    reverse('posts:profile', args=[author_user.username]): '/profile/Author/',
    reverse('posts:post_detail', args=[post.id]): '/posts/1/'

}


class RoutesTests(TestCase):
    def test__routes(self):
        for reversed_path, path in PATHS:
            self.assertEqual(reversed_path, path)
