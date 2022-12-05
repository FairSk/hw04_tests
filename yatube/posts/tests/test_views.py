from django.test import TestCase, Client
from django.urls import reverse

from ..models import Group, Post, User


class ViewsTest(TestCase):
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
            author=ViewsTest.author,
            group=ViewsTest.group
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(ViewsTest.author)

    def test_index_template(self):
        response = self.authorized_client.get(reverse('posts:index'))
        self.assertTemplateUsed(response, 'posts/index.html')

    def test_group_list_template(self):
        response = (self.authorized_client.get(
            reverse('posts:group_posts', args=[ViewsTest.group.slug])))
        self.assertTemplateUsed(response, 'posts/group_list.html')

    def test_profile_template(self):
        response = (self.authorized_client.get(
            reverse('posts:profile', args=[ViewsTest.author.username])))
        self.assertTemplateUsed(response, 'posts/profile.html')

    def test_post_detail_template(self):
        response = (self.authorized_client.get(
            reverse('posts:post_detail', args=[ViewsTest.post.id])))
        self.assertTemplateUsed(response, 'posts/post_detail.html')

    def test_post_edit_template(self):
        response = (self.authorized_client.get(
            reverse('posts:post_edit', args=[ViewsTest.post.id])))
        self.assertTemplateUsed(response, 'posts/post_create.html')

    def test_post_create_template(self):
        response = (self.authorized_client.get(
            reverse('posts:post_create')))
        self.assertTemplateUsed(response, 'posts/post_create.html')

    def test_index_paginator(self):
        response = self.authorized_client.get(reverse('posts:index'))
        self.assertEqual(len(response.context['page_obj']),
                         Post.objects.count())

    def test_profile_paginator(self):
        response = (self.authorized_client.get(
            reverse('posts:profile', args=[ViewsTest.author.username])))
        self.assertEqual(len(response.context['page_obj']),
                         Post.objects.filter(author=ViewsTest.author).count())

    def test_group_list_paginator(self):
        response = (self.authorized_client.get(
            reverse('posts:group_posts', args=[ViewsTest.group.slug])))
        self.assertEqual(len(response.context['page_obj']),
                         Post.objects.filter(group=ViewsTest.group).count())

    def test_index_context(self):
        response = self.authorized_client.get(reverse('posts:index'))
        current_post = response.context['page_obj'][0]
        PARAMS = {
            'text': 'Тестовый текст',
            'author': ViewsTest.author,
            'group': ViewsTest.group
        }
        for parameter, expected_value in PARAMS.items():
            with self.subTest(parameter=parameter):
                self.assertEqual(
                    getattr(current_post, parameter), expected_value)

    def test_group_post_context(self):
        response = (self.authorized_client.get(reverse(
            'posts:group_posts', args=['group-slug'])))
        group = response.context['group']
        posts = response.context['page_obj'][0]
        self.assertEqual(group, ViewsTest.group)
        self.assertEqual(posts.text, 'Тестовый текст')
        self.assertEqual(posts.group, ViewsTest.group)
        self.assertEqual(posts.author, ViewsTest.author)

    def test_profile_context(self):
        response = (self.authorized_client.get(reverse(
            'posts:profile', args=[ViewsTest.author.username])))
        author = response.context['author']
        posts = response.context['page_obj'][0]
        self.assertEqual(author, ViewsTest.author)
        self.assertEqual(posts.text, 'Тестовый текст')
        self.assertEqual(posts.group, ViewsTest.group)
        self.assertEqual(posts.author, ViewsTest.author)

    def text_post_detail_context(self):
        response = (self.authorized_client.get(reverse(
            'posts:post_detail', args=[ViewsTest.post.id])))
        posts = response.context['page_obj'][0]
        self.assertEqual(posts.text, 'Тестовый текст')
        self.assertEqual(posts.group, ViewsTest.group)
        self.assertEqual(posts.author, ViewsTest.author)
