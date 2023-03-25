from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from datetime import datetime

from posts.forms import PostForm
from posts.models import Post, Group


class PostsViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.authorized_client = Client()
        cls.user = User.objects.create_user(username='test', password='test')
        cls.authorized_client.force_login(cls.user)
        cls.group = Group.objects.create(
            title='test',
            slug='test',
            description='test')
        list_of_posts = [
            Post(text=f'test-{i}',
                 author=cls.user,
                 group=cls.group,
                 pub_date=datetime.now())
            for i in range(13)
        ]
        Post.objects.bulk_create(list_of_posts)
        cls.post = Post.objects.first()

    def test_pages_uses_correct_template(self):
        """Тест использования страницами корректных шаблонов"""
        templates_pages_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_list', kwargs={'slug': self.group.slug}):
                'posts/group_list.html',
            reverse('posts:profile', kwargs={'username': self.user.username}):
                'posts/profile.html',
            reverse('posts:post_detail', kwargs={'post_id': self.post.id}):
                'posts/post_detail.html',
            reverse('posts:post_edit', kwargs={'post_id': self.post.id}):
                'posts/create_post.html',
            reverse('posts:post_create'): 'posts/create_post.html',
        }
        for url, template_name in templates_pages_names.items():
            response = self.authorized_client.get(url)
            self.assertTemplateUsed(response, template_name)

    def test_index_show_correct_context(self):
        """Тест использования контекста главной страницы"""
        response = self.authorized_client.get(reverse('posts:index'))
        self.assertEqual(list(response.context['page_obj']),
                         list(Post.objects.all())[:10])

    def test_group_list_show_correct_context(self):
        """Тест использования контекста списка постов в группе"""
        response = self.authorized_client.get(
            reverse('posts:group_list', kwargs={'slug': self.group.slug}))
        self.assertEqual(list(response.context['page_obj']),
                         list(Post.objects.filter(group=self.group)[:10]))

    def test_profile_show_correct_context(self):
        """Тест использования контекста профиля пользователя"""
        response = self.authorized_client.get(
            reverse('posts:profile',
                    kwargs={'username': self.user.username}))
        self.assertEqual(list(response.context['page_obj']),
                         list(Post.objects.filter(author=self.user)[:10]))

    def test_post_detail_show_correct_context(self):
        """Тест использования контекста поста по id"""
        response = self.authorized_client.get(
            reverse('posts:post_detail', kwargs={'post_id': self.post.id}))
        self.assertEqual(response.context['post'],
                         Post.objects.get(id=self.post.id))

    def test_post_edit_show_correct_context(self):
        """Тест использования контекста при редактировании поста"""
        response = self.authorized_client.get(
            reverse('posts:post_edit', kwargs={'post_id': self.post.id}))
        self.assertEqual(response.context['form'].instance,
                         Post.objects.get(id=self.post.id))

    def test_post_create_show_correct_context(self):
        """Тест использования контекста при создании поста"""
        response = self.authorized_client.get(
            reverse('posts:post_create'))
        self.assertIsInstance(response.context['form'], PostForm)


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.authorized_client = Client()
        cls.user = User.objects.create_user(username='test',
                                            password='test')
        cls.authorized_client.force_login(cls.user)
        cls.group = Group.objects.create(
            title='test',
            slug='test',
            description='test')
        list_of_posts = [
            Post(text=f'test-{i}',
                 author=cls.user,
                 group=cls.group,
                 pub_date=datetime.now())
            for i in range(13)
        ]
        Post.objects.bulk_create(list_of_posts)

    def test_index_first_page_contains_ten_posts(self):
        """Тест пагинатора главной страницы"""
        response = self.authorized_client.get(reverse('posts:index'))
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_index_second_page_contains_three_posts(self):
        """Тест пагинатора главной страницы"""
        response = self.authorized_client.get(
            reverse('posts:index') + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 3)

    def test_group_list_first_page_contains_ten_posts(self):
        """Тест пагинатора списка постов в группе"""
        response = self.authorized_client.get(
            reverse('posts:group_list', kwargs={'slug': self.group.slug}))
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_group_list_second_page_contains_three_posts(self):
        """Тест пагинатора списка постов в группе"""
        response = self.authorized_client.get(
            reverse('posts:group_list',
                    kwargs={'slug': self.group.slug}) + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 3)

    def test_profile_first_page_contains_ten_posts(self):
        """Тест пагинатора профиля пользователя"""
        response = self.authorized_client.get(
            reverse('posts:profile',
                    kwargs={'username': self.user.username}))
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_profile_second_page_contains_three_posts(self):
        """Тест пагинатора профиля пользователя"""
        response = self.authorized_client.get(
            reverse('posts:profile',
                    kwargs={'username': self.user.username}) + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 3)
