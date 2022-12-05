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
        cls.anotherGroup = Group.objects.create(
            title='Другой тестовый заголовок',
            description='Другое тестовое описание',
            slug='another-group-slug'
        )
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=ViewsTest.author,
            group=ViewsTest.group
        )
        bulk_list = []
        for i in range(0, 15):
            bulk_list += [Post(
                text='Тестовый текст',
                author=ViewsTest.author,
                group=ViewsTest.group)]
        Post.objects.bulk_create(bulk_list)

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(ViewsTest.author)
        self.POSTS_PER_PAGE = 10

        self.index = reverse('posts:index')
        self.create = reverse('posts:post_create')
        self.edit = reverse('posts:post_edit', args=[self.post.id])
        self.group_post = reverse('posts:group_posts', args=[self.group.slug])
        self.another_group_post = reverse('posts:group_posts',
                                          args=[self.anotherGroup.slug])
        self.profile = reverse('posts:profile', args=[self.author.username])
        self.detail = reverse('posts:post_detail', args=[self.post.id])

    def test_first_page_paginators(self):
        for i in [self.index, self.group_post, self.profile]:
            response = self.client.get(i)
            self.assertEqual(len(response.context['page_obj']),
                             self.POSTS_PER_PAGE)

    def test_second_page_paginators(self):
        for i in [self.index, self.group_post, self.profile]:
            response = self.client.get(i + '?page=2')
            (self.assertEqual(len(response.context['page_obj']),
                              Post.objects.count() - self.POSTS_PER_PAGE))

    def test_contexts_with_paginator(self):
        for i in [self.index, self.group_post, self.profile]:
            response = self.authorized_client.get(i)
            # Без понятия как сделать правку с 'page_obj'
            current_post = response.context['page_obj'][0]
            self.assertEqual(current_post.text, self.post.text)
            self.assertEqual(current_post.author, self.post.author)
            self.assertEqual(current_post.group, self.post.group)

    def text_contexts_other_pages(self):
        response = self.authorized_client.get(self.detail)
        current_post = response.context['post'][0]
        self.assertEqual(current_post.text, self.post.text)
        self.assertEqual(current_post.author, self.post.author)
        self.assertEqual(current_post.group, self.post.group)

    def test_post_is_not_in_other_group(self):
        response = self.authorized_client.get(self.another_group_post)
        current_post = response.context['page_obj']
        self.assertEqual(len(current_post), 0)
