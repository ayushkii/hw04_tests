
from django.shortcuts import redirect, render, get_object_or_404
from .forms import PostForm
from .models import Post, Group, User
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


def index(request):
    post_list = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'post_list': post_list

    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = Post.objects.filter(group=group).order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context,)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    post_list = Post.objects.filter(author=author).order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    counter = post_list.count()
    context = {
        'page_obj': page_obj,
        'author': author,
        'counter': counter,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post_list = Post.objects.filter(author=post.author)
    counter = post_list.count()
    first_thirty = post.__str__()
    context = {
        'post': post,
        'counter': counter,
        'first_thirty': first_thirty,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', username=request.user)
    context = {
        'is_edit': False,
        'groups': Group.objects.all(),
        'form': form,
    }
    return render(request, 'posts/create_post.html', context)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return redirect('posts:post_detail', post.id)
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save(commit=True)
        return redirect('posts:post_detail', post.id)
    context = {
        'is_edit': True,
        'groups': Group.objects.all(),
        'form': form,
        'post': post
    }
    return render(request, 'posts/create_post.html', context)
