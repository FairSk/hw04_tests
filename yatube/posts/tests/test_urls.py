from django.test import TestCase, Client
from django.urls import reverse

from ..models import Group, Post, User

SLUG = 'group-slug'
USERNAME = 'Author'
INDEX = reverse('posts:index')
CREATE = reverse('posts:post_create')
GROUP_POST = reverse('posts:group_posts', args=[SLUG])
PROFILE_ULR = reverse('posts:profile', args=[USERNAME])


class URLSTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author_user = User.objects.create(username=USERNAME)
        cls.no_author = User.objects.create(username='NotAuthor')
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=URLSTests.author_user
        )
        cls.group = Group.objects.create(
            title='Тестовый заголовок',
            description='Тестовое описание',
            slug='group-slug'
        )
        cls.EDIT = reverse('posts:post_edit', args=[URLSTests.post.id])
        cls.DETAIL_URL = reverse('posts:post_detail', args=[URLSTests.post.id])

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.not_author = Client()
        self.authorized_client.force_login(self.author_user)
        self.not_author.force_login(self.no_author)

    def test_pages_access_for_guest(self):
        ACCESSES = [
            (INDEX, self.guest_client, 200),
            (GROUP_POST, self.guest_client, 200),
            (PROFILE_ULR, self.guest_client, 200),
            (CREATE, self.guest_client, 302),
            (self.DETAIL_URL, self.guest_client, 200),
            (self.EDIT, self.guest_client, 302),
            (INDEX, self.authorized_client, 200),
            (GROUP_POST, self.authorized_client, 200),
            (PROFILE_ULR, self.authorized_client, 200),
            (CREATE, self.authorized_client, 200),
            (self.DETAIL_URL, self.authorized_client, 200),
            (self.EDIT, self.authorized_client, 200),
            ('/404/', self.authorized_client, 404),
            (self.EDIT, self.not_author, 302)
        ]
        for url, user, expected_code in ACCESSES:
            with self.subTest(url=url):
                response = user.get(url)
                self.assertEqual(response.status_code, expected_code)

    def test_redirects(self):
        REDIRECTS = [
            (self.EDIT, self.not_author, self.DETAIL_URL),
            # Я ваще без понятия как в реверс сделать передать аргумент
            # '?next=/posts/1/edit/'
            (CREATE, self.guest_client, (reverse('users:login')
                                         + '?next=/create/')),
            (self.EDIT, self.guest_client, (reverse('users:login')
                                            + '?next=/posts/1/edit/')),
        ]
        for url, user, redirect_page in REDIRECTS:
            with self.subTest(url=url):
                response = user.get(url)
                self.assertRedirects(response, redirect_page)

    def test_templates(self):
        TEMPLATES = {
            INDEX: 'posts/index.html',
            GROUP_POST: 'posts/group_list.html',
            PROFILE_ULR: 'posts/profile.html',
            CREATE: 'posts/post_create.html',
            self.DETAIL_URL: 'posts/post_detail.html',
            self.EDIT: 'posts/post_create.html'
        }
        for request, expected_template in TEMPLATES.items():
            with self.subTest(request=request):
                response = self.authorized_client.get(request)
                self.assertTemplateUsed(response, expected_template)
