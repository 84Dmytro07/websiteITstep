from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django import forms
from django.contrib.auth.forms import UserCreationForm



class Category(models.Model):
    name = models.CharField(max_length=30, verbose_name="Назва")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Опис")
    published_date = models.DateTimeField(default=timezone.now, verbose_name="Дата публікації")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категорія")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    image1 = models.ImageField(upload_to='post_images/', blank=True, null=True, verbose_name="Фото 1")
    image2 = models.ImageField(upload_to='post_images/', blank=True, null=True, verbose_name="Фото 2")
    image3 = models.ImageField(upload_to='post_images/', blank=True, null=True, verbose_name="Фото 3")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Пости"


class Comment(models.Model):
    post = models.ForeignKey('Post', related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    ##user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.text

class Subscription(models.Model):
    email = models.EmailField(unique=True)
    created_date = models.DateTimeField(default=timezone.now)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='user_avatar', blank=True, null=True)
    about_user = models.CharField(max_length=200, default='default value')




class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class PostPhoto(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,  verbose_name="Пост")
    image = models.ImageField(verbose_name="Фото", upload_to='Post_photo')
    class Meta:
        verbose_name = "Фото"
        verbose_name_plural = "Фотографии"