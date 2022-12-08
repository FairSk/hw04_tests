from django.test import TestCase
from django.urls import reverse

SLUG = 'group-slug'
USERNAME = 'Author'
POST_ID = 1
PATHS = [
    ('index', '/', [None]),
    ('post_create', '/create/', [None]),
    ('group_posts', '/group/group-slug/', [SLUG]),
    ('profile', '/profile/Author/', [USERNAME]),
    ('post_edit', '/posts/1/edit/', [POST_ID]),
    ('post_detail', '/posts/1/', [POST_ID])
]


class RoutesTests(TestCase):
    def test_routes(self):
        for url, path, arg in PATHS:
            with self.subTest(path=path):
                if arg[0] is None:
                    response = reverse(f'posts:{url}')
                else:
                    response = reverse(f'posts:{url}', args=arg)
                self.assertEqual(response, path)
