from django.test import TestCase, Client
from django.test import TestCase
from django.urls import reverse

from ..models import Group, Post, User

SLUG = 'group-slug'
USERNAME = 'Author'
index = reverse('posts:index')
create = reverse('posts:post_create')
group_post = reverse('posts:group_posts', args=[SLUG])
profile = reverse('posts:profile', args=[USERNAME])


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
        self.edit = reverse('posts:post_edit', args=[self.post.id])
        self.detail = reverse('posts:post_detail', args=[self.post.id])

    def test_create_post_form(self):
        before_creating = Post.objects.count()
        form_data = {
            'text': 'Текст для нового поста',
            'group': self.group.id
        }
        response = (self.authorized_client.post(create,
                                                data=form_data, follow=True))
        current_post = response.context['page_obj'][0]
        creating_cheker = Post.objects.filter(text=form_data['text']).exists()
        after_creating = Post.objects.count()
        self.assertTrue(creating_cheker)
        self.assertEqual(current_post.text, form_data['text'])
        self.assertEqual(current_post.author, self.author)
        self.assertEqual(current_post.group.id, form_data['group'])
        self.assertEqual(before_creating + 1, after_creating)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, profile)

    def test_edit_post_form(self):
        form_data = {
            'text': 'Текст для измененного поста',
            'group': self.anotherGroup.id
        }
        response = (self.authorized_client.post(self.edit,
                                                data=form_data, follow=True))
        current_post = Post.objects.get(id=self.post.id)
        self.assertEqual(current_post.text, form_data['text'])
        self.assertEqual(current_post.author, self.post.author)
        self.assertEqual(current_post.group.id, form_data['group'])
        self.assertRedirects(response, self.detail)
