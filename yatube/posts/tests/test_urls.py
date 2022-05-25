
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from ..models import Group, Post

User = get_user_model()


class PostURLTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='test-user')
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.user,
            group=Group.objects.create(
                title='тестовый тайтл',
                slug='test-slug'
            )
        )

    def setUp(self):
        self.guest_client = Client()  # unauth
        self.authorized_client = Client()  # auth
        self.authorized_client.force_login(self.user)
        self.not_author_user = User.objects.create_user(username='not-author')
        self.not_author_client = Client()  # not-author
        self.not_author_client.force_login(self.not_author_user)

    def test_homepage(self):
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""

        templates_url_names = {
            '/': 'posts/index.html',
            '/group/test-slug/': 'posts/group_list.html',
            '/profile/test-user/': 'posts/profile.html',
            f'/posts/{self.post.id}/': 'posts/post_detail.html',
            '/create/': 'posts/create_post.html',
            # f'/posts/{self.post.id}/edit/': 'posts/create_post.html',
        }
        for address, template in templates_url_names.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)

    def test_urls_any_user(self):
        """любой пользователь получит 404"""
        response = self.guest_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, 404)

    def test_urls_unauth(self):
        """unauth получит что заслуживает"""
        response = self.guest_client.get('/create/')
        self.assertEqual(response.status_code, 302)

    def test_urls_auth(self):
        """auth получит чего достоин"""
        response = self.authorized_client.get('/create/')
        self.assertEqual(response.status_code, 200)

    def test_urls_author(self):
        """моя преле-е-е-есть"""
        response = self.not_author_client.get('/posts/1/edit/')
        self.assertTemplateNotUsed(response, 'create_post.html')
