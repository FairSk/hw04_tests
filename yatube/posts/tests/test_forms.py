from django.test import TestCase, Client
from django.test import TestCase
from django.urls import reverse

from ..models import Group, Post, User


# Сказать честно, я так много раз менял этот код,
# что сам не понимаю, что тут происходит, но тест проходит
class FormsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
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
        cls.author = User.objects.create(username='Author')
        cls.no_author = User.objects.create(username='NotAuthor')
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=FormsTest.author,
            group=FormsTest.group
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

    def test_create_post_form(self):
        before_creating = Post.objects.count()
        form_data = {
            'text': 'Текст для нового поста',
            'group': self.group.id
        }
        response = (self.authorized_client.post(self.create,
                                                data=form_data, follow=True))
        after_creating = Post.objects.count()
        post = Post.objects.get(id='2')
        self.assertEqual(post.text, form_data['text'])
        self.assertEqual(post.author, self.author)
        self.assertEqual(post.group.id, form_data['group'])
        # Не понимаю, как проверить, что изменило количество постов,
        # кроме этого варианта
        self.assertEqual(before_creating + 1, after_creating)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.profile)

    def test_edit_post_form(self):
        form_data = {
            'text': 'Текст для измененного поста',
            'group': self.anotherGroup.id
        }
        response = (self.authorized_client.post(self.edit,
                                                data=form_data, follow=True))
        post = Post.objects.get(id=self.post.id)
        self.assertEqual(post.text, form_data['text'])
        self.assertEqual(post.author, self.author)
        self.assertEqual(post.group.id, form_data['group'])
        self.assertRedirects(response, self.detail)
