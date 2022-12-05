from django.test import TestCase, Client
from django.urls import reverse

from ..models import Group, Post, User


class URLSTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create(username='Author')
        cls.not_author = User.objects.create(username='NotAuthor')
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
        self.authorized_client.force_login(URLSTests.author)
        self.not_author.force_login(URLSTests.not_author)

    def test_index_for_guest(self):
        response = self.guest_client.get(reverse('posts:index'))
        self.assertEqual(response.status_code, 200)

    def test_group_post_for_guest(self):
        response = self.guest_client.get(reverse('posts:group_posts',
                                                 args=['group-slug']))
        self.assertEqual(response.status_code, 200)

    def test_profile_for_guest(self):
        response = self.guest_client.get(reverse('posts:profile',
                                                 args=['Author']))
        self.assertEqual(response.status_code, 200)

    def test_post_create_for_guest(self):
        response = self.guest_client.get(reverse('posts:post_create'))
        self.assertEqual(response.status_code, 302)

    def test_post_detail_for_guest(self):
        response = self.guest_client.get(reverse('posts:post_detail',
                                                 args=['1']))
        self.assertEqual(response.status_code, 200)

    def test_post_edit_for_guest(self):
        response = self.guest_client.get(reverse('posts:post_edit',
                                                 args=['1']))
        self.assertEqual(response.status_code, 302)

    def test_index_for_authorized(self):
        response = self.authorized_client.get(reverse('posts:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/index.html')

    def test_group_post_for_authorized(self):
        response = self.authorized_client.get(reverse('posts:group_posts',
                                                      args=['group-slug']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/group_list.html')

    def test_profile_for_authorized(self):
        response = self.authorized_client.get(reverse('posts:profile',
                                                      args=['Author']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/profile.html')

    def test_post_create_for_authorized(self):
        response = self.authorized_client.get(reverse('posts:post_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/post_create.html')

    def test_post_detail_for_authorized(self):
        response = self.authorized_client.get(reverse('posts:post_detail',
                                                      args=['1']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/post_detail.html')

    def test_post_edit_for_authorized_author(self):
        response = self.authorized_client.get(reverse('posts:post_edit',
                                                      args=['1']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/post_create.html')

    def test_post_edit_for_authorized_non_author(self):
        response = self.not_author.get(reverse('posts:post_edit',
                                               args=[URLSTests.post.id]))
        self.assertEqual(response.status_code, 302)

    def test_page_404(self):
        response = self.authorized_client.get('/404/')
        self.assertEqual(response.status_code, 404)
