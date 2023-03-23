from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from posts.models import Post


class PostCreateTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test', password='test')
        self.client.force_login(self.user)

    def test_create_post(self):
        posts_count = Post.objects.count()
        self.client.post(reverse('posts:post_create'),
                         {'text': 'Test post',
                          'author': self.user.username},
                         follow=True)
        self.assertEqual(Post.objects.count(), posts_count + 1)

    def test_edit_post(self):
        self.post = Post.objects.create(
            text='Test post',
            author=self.user)
        self.client.post(reverse('posts:post_edit', args=(self.post.id,)),
                         {'text': 'Test post edited',
                          'author': self.user.username},
                         follow=True)
        updated_post = Post.objects.get(id=self.post.id)
        self.assertEqual(updated_post.text, 'Test post edited')
