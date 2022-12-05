from django.test import TestCase

from ..models import Post, User, Group


class ModelTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create(username="Author")
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=ModelTests.author
        )
        cls.group = Group.objects.create(
            title='Тестовый заголовок',
            description='Тестовое описание',
            slug='group-slug'
        )

    def test_str_function(self):
        object_names = [
            (ModelTests.post, ModelTests.post.text),
            (ModelTests.group, ModelTests.group.title)
        ]
        for task, text in object_names:
            self.assertEqual(text[:15], str(task))
