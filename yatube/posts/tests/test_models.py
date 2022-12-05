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

    def test_nasd(self):
        object_names = [
            (ModelTests.post, ModelTests.post.text),
            (ModelTests.group, ModelTests.group.title)
        ]
        for i in range(len(object_names)):
            task = object_names[i][0]
            expected_object_name = object_names[i][1][:15]
            self.assertEqual(expected_object_name, str(task))
