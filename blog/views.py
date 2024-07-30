from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now
from django.views import View
from django.contrib import messages
from .forms import PostForm, CommentForm, SubscriptionForm, ProfileUpdateForm
from .models import Post, Category, Comment, Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .forms import UserUpdateForm, RegistrationForm
import logging

logger = logging.getLogger(__name__)

def get_categories():
    all = Category.objects.all()
    count = all.count()
    half = count // 2
    first_half = all[:half]
    second_half = all[half:]
    return {'cats1': first_half, 'cats2': second_half}


def index(request):
    posts = Post.objects.all().order_by("-published_date")
    context = {'posts': posts}
    context.update(get_categories())
    return render(request, "blog/index.html", context)


def category(request, c=None):
    cObj = get_object_or_404(Category, name=c)
    posts = Post.objects.filter(category=cObj).order_by("-published_date")
    context = {'posts': posts}
    context.update(get_categories())
    return render(request, "blog/index.html", context)


def post(request, name=None):
    post = get_object_or_404(Post, title=name)
    comments = Comment.objects.filter(post=post).order_by("-created_date")
    context = {'post': post, 'comments': comments}
    context.update(get_categories())
    return render(request, "blog/post.html", context)


def contact(request):
    context = {}
    context.update(get_categories())
    return render(request, "blog/contact.html", context)


def search(request):
    query = request.GET.get('query')
    posts = Post.objects.filter(Q(content__icontains=query) | Q(title__icontains(query)))
    context = {'posts': posts}
    context.update(get_categories())
    return render(request, "blog/index.html", context)


@login_required
def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.published_date = now()
            post.save()
            return redirect('index')
    else:
        form = PostForm()
    context = {'form': form}
    context.update(get_categories())
    return render(request, "blog/create.html", context)


@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.author = request.user.username
            comment.save()
            logger.info("Comment saved successfully")
            return redirect('post_detail', post_id=post.id)
        else:
            logger.warning("Form is not valid: %s", form.errors)
    else:
        form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'form': form,
    }
    context.update(get_categories())
    return render(request, "blog/post_detail.html", context)


def subscribe(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main')
    else:
        form = SubscriptionForm()

    context = {'form': form}
    context.update(get_categories())
    return render(request, 'blog/subscribe.html', context)


@login_required
def profile(request):
    # profile_data = Profile.objects.get(user=request.user)
    # context = {'profile_data':profile_data}
    # context.update()
    return render(request, 'blog/profile.html')


@login_required
def update_profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'blog/update_profile.html', {'user_form': user_form, 'profile_form': profile_form})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Вы успешно зарегистрировались!')
                return redirect('profile')
            else:
                messages.error(request, 'Ошибка аутентификации, попробуйте снова.')
        else:
            messages.error(request, 'Ошибка в форме, проверьте введенные данные.')
    else:
        form = RegistrationForm()
    return render(request, 'blog/registration_user.html', {'form': form})

class MyLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('main')
