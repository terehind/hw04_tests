from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from ..models import Post


class PostCreateTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test', password='test')
        self.client.force_login(self.user)

    def test_create_post(self):
        initial_count = Post.objects.count()
        response = self.client.post(reverse('posts:post_create'),
                                    {'text': 'Test post',
                                     'author': self.user.username},
                                    follow=True)
        self.assertEqual(response.status_code, 302)
        post_count = Post.objects.count()
        self.assertEqual(post_count, initial_count + 1)

    def test_edit_post(self):
        self.client.post(reverse('posts:post_create'),
                         {'text': 'Test post',
                          'author': self.user.username},
                         follow=True)
        self.client.post(reverse('posts:post_edit', args=(self.post_id,)),
                         {'text': 'Test post edited',
                          'author': self.user.username},
                         follow=True)
        updated_post = Post.objects.get(id=self.post_id)
        self.assertEqual(updated_post.text, 'Test post edited')
