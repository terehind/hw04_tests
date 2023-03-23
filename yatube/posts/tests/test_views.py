from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from ..models import Post, Group


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
        cls.post = Post.objects.create(
            text='test',
            author=cls.user,
            group=cls.group,
        )

    def test_pages_uses_correct_template(self):
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
        response = self.authorized_client.get(reverse('posts:index'))
        self.assertEqual(response.context['page_obj'],
                         Post.objects.select_related('author', 'group')
                         .all()[:10])

    def test_group_list_show_correct_context(self):
        response = self.authorized_client.get(
            reverse('posts:group_list', kwargs={'slug': self.group.slug}))
        self.assertEqual(response.context['page_obj'],
                         Post.objects.filter(group=self.group).select_related(
                             'author', 'group')[:10])

    def test_profile_show_correct_context(self):
        response = self.authorized_client.get(
            reverse('posts:profile', kwargs={'username': self.user.username}))
        self.assertEqual(response.context['page_obj'],
                         Post.objects.filter(author=self.user).select_related(
                             'author', 'group')[:10])

    def test_post_detail_show_correct_context(self):
        response = self.authorized_client.get(
            reverse('posts:post_detail', kwargs={'post_id': self.post.id}))
        self.assertEqual(response.context['post'],
                         Post.objects.get(id=self.post.id))

    def test_post_edit_show_correct_context(self):
        response = self.authorized_client.get(
            reverse('posts:post_edit', kwargs={'post_id': self.post.id}))
        self.assertEqual(response.context['post'],
                         Post.objects.get(id=self.post.id))

    def test_post_create_show_correct_context(self):
        response = self.authorized_client.get(
            reverse('posts:post_create'))
        self.assertEqual(response.context['post'],
                         Post.objects.get(id=self.post.id))


class PaginatorViewsTest(TestCase):
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
        for i in range(13):
            Post.objects.create(
                text=f'test-{i}',
                author=cls.user,
                group=cls.group,
            )
        cls.posts = Post.objects.all().select_related('author', 'group')

    def test_index_first_page_contains_ten_posts(self):
        response = self.authorized_client.get(reverse('posts:index'))
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_index_second_page_contains_three_posts(self):
        response = self.authorized_client.get(
            reverse('posts:index') + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 3)

    def test_group_list_first_page_contains_ten_posts(self):
        response = self.authorized_client.get(
            reverse('posts:group_list', kwargs={'slug': self.group.slug}))
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_group_list_second_page_contains_three_posts(self):
        response = self.authorized_client.get(
            reverse('posts:group_list',
                    kwargs={'slug': self.group.slug}) + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 3)

    def test_profile_first_page_contains_ten_posts(self):
        response = self.authorized_client.get(
            reverse('posts:profile', kwargs={'username': self.user.username}))
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_profile_second_page_contains_three_posts(self):
        response = self.authorized_client.get(
            reverse('posts:profile',
                    kwargs={'username': self.user.username}) + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 3)
