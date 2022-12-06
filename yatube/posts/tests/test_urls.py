from django.test import TestCase, Client
from django.urls import reverse

from ..models import Group, Post, User

SLUG = 'group-slug'
USERNAME = 'Author'
index = reverse('posts:index')
create = reverse('posts:post_create')
group_post = reverse('posts:group_posts', args=[SLUG])
profile = reverse('posts:profile', args=[USERNAME])


class URLSTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author_user = User.objects.create(username='Author')
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

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.not_author = Client()
        self.authorized_client.force_login(self.author_user)
        self.not_author.force_login(self.no_author)
        self.edit = reverse('posts:post_edit', args=[self.post.id])
        self.detail = reverse('posts:post_detail', args=[self.post.id])

    def test_pages_access_for_guest(self):
        ACCESSES = {
            index: 200,
            group_post: 200,
            profile: 200,
            create: 302,
            self.detail: 200,
            self.edit: 302,
        }
        for request, expected_code in ACCESSES.items():
            response = self.guest_client.get(request)
            self.assertEqual(response.status_code, expected_code)

    def test_pages_access_for_not_author(self):
        response = self.not_author.get(self.edit)
        self.assertEqual(response.status_code, 302)

    def test_pages_access_for_author(self):
        ACCESSES = {
            index: 200,
            group_post: 200,
            profile: 200,
            create: 200,
            self.detail: 200,
            self.edit: 200,
            '/404/': 404,
        }
        for request, expected_code in ACCESSES.items():
            response = self.authorized_client.get(request)
            self.assertEqual(response.status_code, expected_code)

    def test_redirects(self):
        REDIRECTS = {
            self.not_author.get(self.edit): self.detail,
            # Я тут попытался как-то изменить реверс ссылку,
            # но не получилось
            self.guest_client.get(create): (reverse('users:login')
                                            + '?next=/create/'),
            self.guest_client.get(self.edit): (reverse('users:login')
                                               + '?next=/posts/1/edit/')
        }
        for request, expected_redirect in REDIRECTS.items():
            response = request
            self.assertRedirects(response, expected_redirect)

    def test_templates(self):
        TEMPLATES = {
            index: 'posts/index.html',
            group_post: 'posts/group_list.html',
            profile: 'posts/profile.html',
            create: 'posts/post_create.html',
            self.detail: 'posts/post_detail.html',
            self.edit: 'posts/post_create.html'
        }
        for request, expected_template in TEMPLATES.items():
            response = self.authorized_client.get(request)
            self.assertTemplateUsed(response, expected_template)
