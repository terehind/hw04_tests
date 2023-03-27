from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from posts.models import Post, Group


class PostCreateTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test', password='test')
        self.client.force_login(self.user)
        self.group = Group.objects.create(title='test group', slug='test')
        self.post = Post.objects.create(
            text='Test post',
            author=self.user,
            group=self.group)

    def test_create_post(self):
        """Тест формы создания поста"""
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Test post',
            'group': self.group.id,
        }
        self.client.post(reverse('posts:post_create'),
                         form_data,
                         follow=True)
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertTrue(
            Post.objects.filter(
                text=form_data['text'],
                group=form_data['group'],
            ).exists())
        new_post = Post.objects.latest('id')
        self.assertEqual(new_post.text, form_data['text'])
        self.assertEqual(new_post.author, self.user)
        self.assertEqual(new_post.group, self.group)

    def test_edit_post(self):
        """Тест формы редактирования поста"""
        posts_count = Post.objects.count()
        old_group = self.group
        new_group = Group.objects.create(title='new group', slug='new_group')
        form_data = {
            'text': 'Test post edited',
            'group': new_group.id,
        }
        self.client.post(reverse('posts:post_edit', args=[self.post.id]),
                         form_data,
                         follow=True)
        self.assertEqual(Post.objects.count(), posts_count)
        self.assertTrue(
            Post.objects.filter(
                text=form_data['text'],
                group=form_data['group'],
            ).exists())
        self.assertEqual(old_group.posts.count(), 0)
        self.assertEqual(new_group.posts.count(), 1)
