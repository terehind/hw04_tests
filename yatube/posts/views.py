from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from .models import Post, Group
from .forms import PostForm
from .utils import paginator


def index(request, count_of_posts=10):
    posts = Post.objects.select_related('author', 'group').all()
    page_obj = paginator(request, posts, count_of_posts)
    template = 'posts/index.html'
    context = {'page_obj': page_obj,
               }
    return render(request, template, context)


def group_posts(request, slug, count_of_posts=10):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).select_related('author', 'group')
    page_obj = paginator(request, posts, count_of_posts)
    template = 'posts/group_list.html'
    context = {'group': group,
               'page_obj': page_obj,
               }
    return render(request, template, context)


def profile(request, username, count_of_posts=10):
    author = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=author).select_related('author',
                                                              'group')
    page_obj = paginator(request, posts, count_of_posts)
    template = 'posts/profile.html'
    context = {
        'author': author,
        'posts': posts,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def post_detail(request, post_id, size_of_title=30):
    post = get_object_or_404(Post, pk=post_id)
    title = post.text[:size_of_title]
    count_of_posts = Post.objects.filter(author=post.author).count()
    template = 'posts/post_detail.html'
    context = {
        'post': post,
        'title': title,
        'count_of_posts': count_of_posts,
    }
    return render(request, template, context)


@login_required
def post_create(request):
    form = PostForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', username=request.user.username)
    template = 'posts/create_post.html'
    context = {
        'form': form,
        'is_edit': False,
    }
    return render(request, template, context)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        return redirect('posts:post_detail', post_id=post_id)
    form = PostForm(request.POST or None, instance=post)
    if request.method == 'POST' and form.is_valid():
        post = form.save(commit=False)
        post.save()
        return redirect('posts:post_detail', post_id=post_id)
    template = 'posts/create_post.html'
    context = {
        'form': form,
        'post': post,
        'is_edit': True,
    }
    return render(request, template, context)
