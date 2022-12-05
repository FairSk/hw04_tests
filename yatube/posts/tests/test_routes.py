from django.test import TestCase
from django.urls import resolve


class RoutesTests(TestCase):
    def test_index_route(self):
        PATHS = {
            '/': 'posts:index',
            '/create/': 'posts:post_create',
            '/posts/1/edit/': 'posts:post_edit',
            '/group/group-slug/': 'posts:group_posts',
            '/profile/Author/': 'posts:profile',
            '/posts/1/': 'posts:post_detail'
        }
        for resolver, url in PATHS.items():
            with self.subTest(resolver=resolver):
                resolver = resolve(resolver)
                self.assertEqual(resolver.view_name, url)
