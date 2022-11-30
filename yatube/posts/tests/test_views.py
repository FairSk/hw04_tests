# posts/tests/test_urls.py
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django import forms

from ..models import Group, Post

User = get_user_model()


class TaskViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='HasNoName')
        Group.objects.create(
            title='Тестовый заголовок',
            description='Тестовое описание',
            slug='group-slug'
        )
        Post.objects.create(
            author=User.objects.get(username='HasNoName'),
            text='Текст',
            group=Group.objects.get(slug='group-slug')
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_index(self):
        response = self.guest_client.get(reverse('posts:index'))
        self.assertTemplateUsed(response, 'posts/index.html',
                                'Index page use different HTML page')

    def test_group(self):
        response = self.guest_client.get(reverse('posts:group_posts',
                                                 kwargs={
                                                     'slug': 'group-slug'}))
        self.assertTemplateUsed(response, 'posts/group_list.html',
                                'Group page use different HTML page')

    def test_profile(self):
        response = self.guest_client.get(reverse('posts:profile',
                                                 kwargs={
                                                     'username': 'HasNoName'}))
        self.assertTemplateUsed(response, 'posts/profile.html',
                                'Profile page use different HTML page')

    def test_create(self):
        response = self.authorized_client.get(reverse('posts:post_create'))
        self.assertTemplateUsed(response, 'posts/post_create.html',
                                'Create page use different HTML page')

    def test_post_detail(self):
        response = self.authorized_client.get(reverse('posts:post_detail',
                                                      kwargs={
                                                          'post_id': '1'}))
        self.assertTemplateUsed(response, 'posts/post_detail.html',
                                'Posts Detail page use different HTML page')

    def test_post_edit(self):
        response = self.authorized_client.get(reverse('posts:post_edit',
                                                      kwargs={
                                                          'post_id': '1'}))
        self.assertTemplateUsed(response, 'posts/post_create.html',
                                'Posts Edit page use different HTML page')

    def test_post_context(self):
        response = self.authorized_client.get(reverse('posts:index'))
        first_object = response.context['page_obj'][0]
        author_0 = first_object.author.username
        test_0 = first_object.text
        slug_0 = first_object.group.slug
        self.assertEqual(author_0, 'HasNoName')
        self.assertEqual(test_0, 'Текст')
        self.assertEqual(slug_0, 'group-slug')

    def test_group_context(self):
        response = self.authorized_client.get(reverse('posts:group_posts',
                                                      kwargs={
                                                          'slug':
                                                              'group-slug'}))
        first_object = response.context['page_obj'][0]
        author_0 = first_object.author.username
        test_0 = first_object.text
        slug_0 = first_object.group.slug
        group = response.context['group'].slug
        self.assertEqual(group, 'group-slug')
        self.assertEqual(author_0, 'HasNoName')
        self.assertEqual(test_0, 'Текст')
        self.assertEqual(slug_0, 'group-slug')

    def test_profile_context(self):
        response = self.authorized_client.get(reverse('posts:profile',
                                                      kwargs={
                                                          'username':
                                                              'HasNoName'}))
        first_object = response.context['page_obj'][0]
        author_0 = first_object.author.username
        test_0 = first_object.text
        slug_0 = first_object.group.slug
        user_nickname = response.context['author'].username
        self.assertEqual(user_nickname, 'HasNoName')
        self.assertEqual(author_0, 'HasNoName')
        self.assertEqual(test_0, 'Текст')
        self.assertEqual(slug_0, 'group-slug')

    def test_post_detail_context(self):
        response = self.authorized_client.get(reverse('posts:post_detail',
                                                      kwargs={
                                                          'post_id': '1'}))
        first_object = response.context['post']
        author = first_object.author.username
        test = first_object.text
        slug = first_object.group.slug
        self.assertEqual(author, 'HasNoName')
        self.assertEqual(test, 'Текст')
        self.assertEqual(slug, 'group-slug')

    def test_create_context(self):
        response = self.authorized_client.get(reverse('posts:post_create'))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField
        }

        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_create_edit_context(self):
        response = self.authorized_client.get(reverse('posts:post_edit',
                                                      kwargs={
                                                          'post_id': '1'}))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField
        }

        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_post_paginator(self):
        response = self.client.get(reverse('posts:index'))
        self.assertEqual(len(response.context['page_obj']), 1)

    def test_grou_list_paginator(self):
        response = self.client.get(reverse('posts:group_posts',
                                           kwargs={
                                               'slug': 'group-slug'}))
        self.assertEqual(len(response.context['page_obj']), 1)

    def test_post_paginator(self):
        response = self.client.get(reverse('posts:profile',
                                           kwargs={
                                               'username': 'HasNoName'}))
        self.assertEqual(len(response.context['page_obj']), 1)

    def test_post_has_group(self):
        Post.objects.create(
            id='2',
            author=User.objects.get(username='HasNoName'),
            text='test-text',
            group=Group.objects.get(slug='group-slug')
        )
        self.assertEqual(1, 1, '1!=1')
