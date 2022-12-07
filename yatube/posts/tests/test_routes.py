from django.test import TestCase
from django.urls import reverse

SLUG = 'group-slug'
USERNAME = 'Author'
POST_ID = '1'
INDEX = reverse('posts:index')
CREATE = reverse('posts:post_create')
GROUP_POST = reverse('posts:group_posts', args=[SLUG])
PROFILE_ULR = reverse('posts:profile', args=[USERNAME])
EDIT_URL = reverse('posts:post_edit', args=[POST_ID])
DETAIL_URL = reverse('posts:post_detail', args=[POST_ID])
PATHS = {
    INDEX: '/',
    CREATE: '/create/',
    EDIT_URL: '/posts/1/edit/',
    GROUP_POST: '/group/group-slug/',
    PROFILE_ULR: '/profile/Author/',
    DETAIL_URL: '/posts/1/'
}


class RoutesTests(TestCase):
    def test_routes(self):
        for reversed_path, path in PATHS.items():
            self.assertEqual(reversed_path, path)
