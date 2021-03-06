
from django.contrib.auth import get_user_model
from django.test import TestCase
from ..models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовая пост',
        )

    def test_post_model_has_correct_str_method(self):
        post = PostModelTest.post
        self.assertEqual(post.text[:15], post.__str__())

    def test_group_model_has_correct_str_method(self):
        group = PostModelTest.group
        title = group.title
        self.assertEqual(title, group.__str__())
