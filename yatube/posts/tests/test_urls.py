from django.test import TestCase, Client
from django.urls import reverse

from ..models import Group, Post, User


# Надеюсь в этот раз я понял, что нужно проверять в контекстах
class URLSTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create(username='Author')
        cls.no_author = User.objects.create(username='NotAuthor')
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=URLSTests.author
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
        self.authorized_client.force_login(self.author)
        self.not_author.force_login(self.no_author)

        self.index = reverse('posts:index')
        self.create = reverse('posts:post_create')
        self.edit = reverse('posts:post_edit', args=[self.post.id])
        self.group_post = reverse('posts:group_posts', args=[self.group.slug])
        self.profile = reverse('posts:profile', args=[self.author.username])
        self.detail = reverse('posts:post_detail', args=[self.post.id])

        self.ACCESSES = {
            self.not_author.get(self.edit): 302,
            self.guest_client.get(self.index): 200,
            self.guest_client.get(self.group_post): 200,
            self.guest_client.get(self.profile): 200,
            self.guest_client.get(self.create): 302,
            self.guest_client.get(self.detail): 200,
            self.guest_client.get(self.edit): 302,
            self.authorized_client.get(self.index): 200,
            self.authorized_client.get(self.group_post): 200,
            self.authorized_client.get(self.profile): 200,
            self.authorized_client.get(self.create): 200,
            self.authorized_client.get(self.detail): 200,
            self.authorized_client.get(self.edit): 200,
            self.authorized_client.get('/404/'): 404,
        }

        self.REDIRECTS = {
            self.not_author.get(self.edit): self.detail,
            self.guest_client.get(self.create): (reverse('users:login')
                                                 + '?next=/create/'),
            self.guest_client.get(self.edit): (reverse('users:login')
                                               + '?next=/posts/1/edit/')
        }

        self.TEMPLATES = {
            self.authorized_client.get(self.index): 'posts/index.html',
            self.authorized_client.get(self.group_post):
                'posts/group_list.html',
            self.authorized_client.get(self.profile): 'posts/profile.html',
            self.authorized_client.get(self.create): 'posts/post_create.html',
            self.authorized_client.get(self.detail): 'posts/post_detail.html',
            self.authorized_client.get(self.edit): 'posts/post_create.html',
        }

    def test_pages_access(self):
        for request, expected_code in self.ACCESSES.items():
            response = request
            self.assertEqual(response.status_code, expected_code)

    def test_redirects(self):
        for request, expected_redirect in self.REDIRECTS.items():
            response = request
            self.assertRedirects(response, expected_redirect)

    def test_templates(self):
        for request, expected_template in self.TEMPLATES.items():
            response = request
            self.assertTemplateUsed(response, expected_template)
        
