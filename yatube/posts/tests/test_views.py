from django.test import TestCase, Client
from django.urls import reverse

from ..models import Group, Post, User

# Я в душе не чаю, как в этом файле
# нормально сделать тесты
SLUG = 'group-slug'
ANOTHER_SLUG = 'another-group-slug'
USERNAME = 'Author'
index = reverse('posts:index')
create = reverse('posts:post_create')
group_post = reverse('posts:group_posts', args=[SLUG])
profile = reverse('posts:profile', args=[USERNAME])
another_group_post = reverse('posts:group_posts', args=[ANOTHER_SLUG])


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
        cls.another_group = Group.objects.create(
            title='Другой тестовый заголовок',
            description='Другое тестовое описание',
            slug='another-group-slug'
        )
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=ViewsTest.author,
            group=ViewsTest.group
        )
        bulk_list = ([Post(text=f'Тестовый текст для паджинатора №{item}',
                           author=ViewsTest.author, group=ViewsTest.group)
                      for item in range(1, 16)])
        Post.objects.bulk_create(bulk_list)

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(ViewsTest.author)
        self.POSTS_PER_PAGE = 10

        self.edit = reverse('posts:post_edit', args=[self.post.id])
        self.detail = reverse('posts:post_detail', args=[self.post.id])

    def test_first_page_paginators(self):
        for item in [index, group_post, profile]:
            with self.subTest(item=item):
                response = self.authorized_client.get(item)
                self.assertEqual(len(response.context['page_obj']),
                                 self.POSTS_PER_PAGE)

    def test_second_page_paginators(self):
        for item in [index, group_post, profile]:
            response = self.authorized_client.get(item + '?page=2')
            (self.assertEqual(len(response.context['page_obj']),
                              Post.objects.count() - self.POSTS_PER_PAGE))

    def test_contexts_index(self):
        response = self.authorized_client.get(index + '?page=2')
        post = response.context['page_obj'][5]
        self.assertEqual(post.text, self.post.text)
        self.assertEqual(post.author, self.post.author)
        self.assertEqual(post.group, self.post.group)

    def test_contexts_group(self):
        response = self.authorized_client.get(group_post + '?page=2')
        post = response.context['page_obj'][5]
        group = response.context['group']
        self.assertEqual(group, self.group)
        self.assertEqual(post.text, self.post.text)
        self.assertEqual(post.author, self.post.author)
        self.assertEqual(post.group, self.post.group)

    def test_contexts_profile(self):
        response = self.authorized_client.get(profile + '?page=2')
        post = response.context['page_obj'][5]
        author = response.context['author']
        self.assertEqual(author, self.author)
        self.assertEqual(post.text, self.post.text)
        self.assertEqual(post.author, self.post.author)
        self.assertEqual(post.group, self.post.group)

    def text_contexts_other_pages(self):
        response = self.authorized_client.get(self.detail)
        current_post = response.context['post'][0]
        self.assertEqual(current_post.text, self.post.text)
        self.assertEqual(current_post.author, self.post.author)
        self.assertEqual(current_post.group, self.post.group)

    def test_post_is_not_in_other_group(self):
        response = self.authorized_client.get(another_group_post)
        current_post = list(response.context['page_obj'])
        self.assertTrue(self.post not in current_post)
