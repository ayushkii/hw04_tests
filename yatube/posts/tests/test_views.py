# deals/tests/test_views.py
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Post, Group
from django import forms
User = get_user_model()


class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='test-user',
                                            first_name='Тестовый',
                                            last_name='Юзер')
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.user,
            group=Group.objects.create(
                title='тестовый тайтл',
                slug='test-slug'
            )
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    # Проверяем используемые шаблоны
    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        # Собираем в словарь пары "имя_html_шаблона: reverse(name)"
        templates_pages_names = {
            'posts/index.html': reverse('posts:index'),
            'posts/group_list.html': (
                reverse('posts:group_list', kwargs={'slug': 'test-slug'})
            ),
            'posts/profile.html': (
                reverse('posts:profile', kwargs={'username': 'test-user'})
            ),
            'posts/post_detail.html': (
                reverse('posts:post_detail', kwargs={'post_id': '1'})
            ),
            'posts/create_post.html': reverse('posts:post_create')
        }
# Проверяем, что при обращении к name вызывается соответствующий HTML-шаблон
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_post_edit_view(self):
        reverse_name = reverse('posts:post_edit', kwargs={'post_id': '1'})
        response = self.authorized_client.get(reverse_name)
        self.assertTemplateUsed(response, 'posts/create_post.html')

    def test_index_page_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:index'))
        first_object = response.context['page_obj'][0]
        page_text = str(response.context['page_obj'].object_list)
        post_author_0 = first_object.author
        post_group_0 = first_object.group
        self.assertEqual(post_author_0.username, 'test-user')
        self.assertEqual(post_group_0.slug, 'test-slug')
        self.assertIn('Тестовый текст', page_text)

    def test_post_detail_pages_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        response = (self.authorized_client.
                    get(reverse(
                        'posts:post_detail', kwargs={'post_id': '1'}
                    )))
        self.assertEqual(response.context.get('post').author.username,
                         'test-user')
        self.assertEqual(response.context.get('post').text, 'Тестовый текст')
        self.assertEqual(response.context.get('post').group.slug, 'test-slug')

    def test_group_list_pages_show_correct_context(self):
        """group_list работает корректно"""
        response = (self.authorized_client.get(reverse('posts:group_list',
                    kwargs={'slug': 'test-slug'})))
        first_object = response.context['page_obj'][0]
        post_group_0 = first_object.group
        self.assertEqual(post_group_0.slug, 'test-slug')

    def test_profile_pages_show_correct_context(self):
        """profile работает корректно"""
        response = (self.authorized_client.get(reverse('posts:profile',
                    kwargs={'username': 'test-user'})))
        first_object = response.context['page_obj'][0]
        post_author_0 = first_object.author
        self.assertEqual(post_author_0.username, 'test-user')

    def test_post_detail_pasges_show_correct_context(self):
        """post_detail работает корректно"""
        response = (self.authorized_client.get(reverse('posts:post_detail',
                    kwargs={'post_id': '1'})))
        first_object = response.context.get('post')
        post_id_0 = first_object.id
        self.assertEqual(post_id_0, 1)

    def test_create_post_pages_show_correct_context(self):
        """create работает корректно"""
        response = (self.authorized_client.get(reverse('posts:post_create')))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }

    # Проверяем, что типы полей формы в словаре context соответствуют ожиданиям
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_edit_post_pages_show_correct_context(self):
        """edit работает корректно"""
        response = (self.authorized_client.get(reverse('posts:post_edit',
                                                       kwargs={'post_id': 1})))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    # Проверяем, что типы полей формы в словаре context соответствуют ожиданиям
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)


class PaginatorViewsTest(TestCase):
    # Здесь создаются фикстуры: клиент и 13 тестовых записей.
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='test-user',
                                            first_name='Тестовый',
                                            last_name='Юзер')
        cls.group = Group.objects.create(title='test-title',
                                         slug='test-slug')
        for i in range(0, 13):
            cls.post = Post.objects.create(
                text=f'Тестовый текст {i}',
                author=cls.user,
                group=cls.group
            )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_paginator_on_index_page(self):
        response = self.client.get(reverse('posts:index'))
        # Проверка: количество постов на первой странице равно 10.
        self.assertEqual(len(response.context['page_obj']), 10)
        # Проверка: на второй странице должно быть три поста.
        response = self.client.get(reverse('posts:index') + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 3)

    def test_paginator_on_group_list_page(self):
        response = self.client.get(reverse('posts:group_list',
                                           kwargs={'slug': 'test-slug'}))
        self.assertEqual(len(response.context['page_obj']), 10)
        response = self.client.get(reverse('posts:group_list',
                                           kwargs={'slug': 'test-slug'})
                                   + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 3)

    def test_paginator_on_profile_page(self):
        response = self.client.get(reverse('posts:profile',
                                           kwargs={'username': 'test-user'}))
        self.assertEqual(len(response.context['page_obj']), 10)
        response = self.client.get(reverse('posts:profile',
                                           kwargs={'username': 'test-user'})
                                   + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 3)


class PostWithGroupCreationTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user1 = User.objects.create_user(username='test-user1',
                                             first_name='Тестовый',
                                             last_name='Юзер')
        cls.group1 = Group.objects.create(title='test-title1',
                                          slug='test-slug1')
        cls.post1 = Post.objects.create(text='Тестовый текст1',
                                        author=cls.user1,
                                        group=cls.group1)
        cls.group2 = Group.objects.create(title='test-title2',
                                          slug='test-slug2')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user1)

    def test_new_post_on_index_page(self):
        response = (self.authorized_client.get(reverse('posts:index')))
        page_text = str(response.context['page_obj'].object_list)
        self.assertIn('Тестовый текст1', page_text)

    def test_new_post_on_group_page(self):
        response = (self.authorized_client.get(
            reverse('posts:group_list', kwargs={'slug': 'test-slug1'})))
        page_text = str(response.context['page_obj'].object_list)
        self.assertIn('Тестовый текст1', page_text)

    def test_new_post_on_profile_page(self):
        response = (self.authorized_client.get(
            reverse('posts:profile', kwargs={'username': 'test-user1'})))
        page_text = str(response.context['page_obj'].object_list)
        self.assertIn('Тестовый текст1', page_text)

    def test_new_post_on_wrong_group_page(self):
        response = (self.authorized_client.get(
            reverse('posts:group_list', kwargs={'slug': 'test-slug2'})))
        page_text = str(response.context['page_obj'].object_list)
        self.assertNotIn('Тестовый текст1', page_text)
