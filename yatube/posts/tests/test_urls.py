from django.contrib.auth.models import User
from django.test import TestCase, Client
from posts.models import Post, Group


class PostsURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()
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

    def test_index_url(self):
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_group_list_url(self):
        response = self.guest_client.get('/group/test/')
        self.assertEqual(response.status_code, 200)

    def test_profile_url(self):
        response = self.guest_client.get('/profile/test/')
        self.assertEqual(response.status_code, 200)

    def test_post_detail_url(self):
        response = self.guest_client.get('/posts/1/')
        self.assertEqual(response.status_code, 200)

    def test_unexisting_url(self):
        response = self.guest_client.get('/unexisting/')
        self.assertEqual(response.status_code, 404)

    def test_create_post_url(self):
        response = self.authorized_client.get('/create/')
        self.assertEqual(response.status_code, 200)

    def test_edit_post_url(self):
        response = self.authorized_client.get('/posts/1/edit/')
        self.assertEqual(response.status_code, 200)

    def test_create_post_url_redirect_login(self):
        response = self.guest_client.get('/create/', follow=True)
        self.assertRedirects(response, '/auth/login/?next=/create/')

    def test_edit_post_url_redirect_login(self):
        response = self.guest_client.get('/posts/1/edit/', follow=True)
        self.assertRedirects(response, '/auth/login/?next=/posts/1/edit/')

    def test_urls_uses_correct_template(self):
        templates_url_names = {
            '/': 'posts/index.html',
            '/group/test/': 'posts/group_list.html',
            '/profile/test/': 'posts/profile.html',
            '/posts/1/': 'posts/post_detail.html',
            '/posts/1/edit/': 'posts/create_post.html',
            '/create/': 'posts/create_post.html',
        }
        for url, template_name in templates_url_names.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template_name)
