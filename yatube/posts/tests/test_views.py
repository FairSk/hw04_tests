from django.test import TestCase, Client
from django.urls import reverse

from ..models import Group, Post, User
from ..views import POSTS_PER_PAGE

SLUG = 'group-slug'
ANOTHER_SLUG = 'another-group-slug'
USERNAME = 'Author'
INDEX = reverse('posts:index')
CREATE = reverse('posts:post_create')
GROUP_POST = reverse('posts:group_posts', args=[SLUG])
PROFILE_ULR = reverse('posts:profile', args=[USERNAME])
ANOTHER_GROUP_POST = reverse('posts:group_posts', args=[ANOTHER_SLUG])


class ViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create(username=USERNAME)
        cls.group = Group.objects.create(
            title='Тестовый заголовок',
            description='Тестовое описание',
            slug=SLUG
        )
        cls.another_group = Group.objects.create(
            title='Другой тестовый заголовок',
            description='Другое тестовое описание',
            slug=ANOTHER_SLUG
        )
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=ViewsTest.author,
            group=ViewsTest.group
        )
        cls.EDIT = reverse('posts:post_edit', args=[ViewsTest.post.id])
        cls.DETAIL_URL = reverse('posts:post_detail',
                                 args=[ViewsTest.post.id])

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(ViewsTest.author)

    def test_paginators(self):
        Post.objects.bulk_create(
            ([Post(text=f'Тестовый текст для паджинатора №{item}',
                   author=ViewsTest.author, group=ViewsTest.group)
              for item in range(POSTS_PER_PAGE)]))
        PAGINATOR_PAGES = [
            (INDEX, '', POSTS_PER_PAGE),
            (GROUP_POST, '', POSTS_PER_PAGE),
            (PROFILE_ULR, '', POSTS_PER_PAGE),
            (INDEX, '?page=2', Post.objects.count() - POSTS_PER_PAGE),
            (GROUP_POST, '?page=2', Post.objects.count() - POSTS_PER_PAGE),
            (PROFILE_ULR, '?page=2', Post.objects.count() - POSTS_PER_PAGE),
        ]
        for url, page_num, objects in PAGINATOR_PAGES:
            with self.subTest(url=url):
                response = self.authorized_client.get(url + page_num)
                self.assertEqual(len(response.context['page_obj']), objects)

    def test_contexts_other_pages(self):
        URLS = [
            (INDEX, 'page_obj', None),
            (GROUP_POST, 'page_obj', None),
            (GROUP_POST, 'group', self.group),
            (PROFILE_ULR, 'page_obj', None),
            (PROFILE_ULR, 'author', self.author),
            (self.DETAIL_URL, 'post', self.post),
        ]
        for url, context, equals_to in URLS:
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                if equals_to is not None:
                    post = response.context[context]
                    self.assertEqual(post, equals_to)
                else:
                    post = response.context[context][0]
                    self.assertEqual(post.text, self.post.text)
                    self.assertEqual(post.author, self.post.author)
                    self.assertEqual(post.group, self.post.group)

    def test_post_is_not_in_other_group(self):
        response = self.authorized_client.get(ANOTHER_GROUP_POST)
        current_post = response.context['page_obj']
        self.assertNotIn(self.post, current_post)
