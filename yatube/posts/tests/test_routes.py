from django.test import TestCase
from django.urls import reverse

SLUG = 'group-slug'
USERNAME = 'Author'
POST_ID = 1
PATHS = {
    reverse('posts:index'): '/',
    reverse('posts:post_create'): '/create/',
    reverse('posts:group_posts', args=[SLUG]): '/group/group-slug/',
    reverse('posts:profile', args=[USERNAME]): '/profile/Author/',
    reverse('posts:post_edit', args=[POST_ID]): '/posts/1/edit/',
    reverse('posts:post_detail', args=[POST_ID]): '/posts/1/'
}


class RoutesTests(TestCase):
    def test_routes(self):
        for reversed_path, path in PATHS.items():
            with self.subTest(path=path):
                self.assertEqual(reversed_path, path)
