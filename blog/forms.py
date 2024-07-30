from django import forms
from .models import Post, Comment, Subscription, Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'image1', 'image2', 'image3']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ('email',)

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'about_user']

