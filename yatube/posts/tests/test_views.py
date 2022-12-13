from django.test import TestCase, Client
from django.urls import reverse

from ..models import Group, Post, User
from ..views import POSTS_PER_PAGE

SLUG = 'group-slug'
ANOTHER_SLUG = 'another-group-slug'
USERNAME = 'Author'
INDEX_URL = reverse('posts:index')
INDEX_PAGE_2_URL = reverse('posts:index') + '?page=2'
CREATE_URL = reverse('posts:post_create')
GROUP_POST_URL = reverse('posts:group_posts', args=[SLUG])
GROUP_POST_PAGE_2_URL = reverse('posts:group_posts', args=[SLUG]) + '?page=2'
PROFILE_ULR = reverse('posts:profile', args=[USERNAME])
PROFILE_PAGE_2_ULR = reverse('posts:profile', args=[USERNAME]) + '?page=2'
ANOTHER_GROUP_POST_URL = reverse('posts:group_posts', args=[ANOTHER_SLUG])


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
        cls.EDIT_URL = reverse('posts:post_edit', args=[ViewsTest.post.id])
        cls.DETAIL_URL = reverse('posts:post_detail',
                                 args=[ViewsTest.post.id])

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(ViewsTest.author)

    def test_paginators(self):
        Post.objects.bulk_create(
            Post(text=f'Тестовый текст для паджинатора №{item}',
                 author=ViewsTest.author, group=ViewsTest.group)
            for item in range(POSTS_PER_PAGE))
        PAGINATOR_PAGES = [
            (INDEX_URL, POSTS_PER_PAGE),
            (GROUP_POST_URL, POSTS_PER_PAGE),
            (PROFILE_ULR, POSTS_PER_PAGE),
            (INDEX_PAGE_2_URL, Post.objects.count() - POSTS_PER_PAGE),
            (GROUP_POST_PAGE_2_URL, Post.objects.count() - POSTS_PER_PAGE),
            (PROFILE_PAGE_2_ULR, Post.objects.count() - POSTS_PER_PAGE),
        ]
        for url, objects in PAGINATOR_PAGES:
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertEqual(len(response.context['page_obj']), objects)

    def test_contexts_other_pages(self):
        URLS = [
            (INDEX_URL, 'page_obj'),
            (GROUP_POST_URL, 'page_obj'),
            (PROFILE_ULR, 'page_obj'),
            (self.DETAIL_URL, 'post')
        ]
        for url, context in URLS:
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                if context == 'page_obj':
                    paginator_page = response.context.get(context)
                    self.assertEqual(len(list(paginator_page)))
                    post = paginator_page[0]
                elif context == 'post':
                    post = response.context.get(context)
                self.assertEqual(post.id, self.post.id)
                self.assertEqual(post.text, self.post.text)
                self.assertEqual(post.author, self.post.author)
                self.assertEqual(post.group, self.post.group)

    def test_context_group_in_group(self):
        response = self.authorized_client.get(GROUP_POST_URL)
        group = response.context['group']
        self.assertEqual(group, self.group)
        self.assertEqual(group.title, self.group.title)
        self.assertEqual(group.slug, self.group.slug)
        self.assertEqual(group.description, self.group.description)

    def test_context_author_in_profile(self):
        response = self.authorized_client.get(PROFILE_ULR)
        self.assertEqual(response.context['author'], self.author)

    def test_post_is_not_in_other_group(self):
        response = self.authorized_client.get(ANOTHER_GROUP_POST_URL)
        post = response.context['page_obj']
        self.assertNotIn(self.post, post)
