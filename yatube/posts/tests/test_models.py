from django.contrib.auth.models import User
from django.test import TestCase
from posts.models import Group, Post


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
            text='Тестовый пост ' * 5,
        )

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__"""
        self.assertEqual(str(self.post), self.post.text[:15])
        self.assertEqual(str(self.group), self.group.title)

    def test_models_have_correct_field_names_and_help_texts(self):
        """Проверяем, у моделей корректность полей verbose_name и
        help_text"""
        self.assertEqual(self.post._meta.get_field('text').verbose_name,
                         'Текст поста')
        self.assertEqual(self.post._meta.get_field('group').verbose_name,
                         'Группа')
        self.assertEqual(self.post._meta.get_field('text').help_text,
                         'Введите текст поста')
        self.assertEqual(self.post._meta.get_field('group').help_text,
                         'Выберите группу')
