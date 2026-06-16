from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Post, Category, Comment, Like
from .forms import PostForm, CommentForm


def home_view(request):
    posts = Post.objects.filter(status='published').order_by('-created_at')
    categories = Category.objects.all()

    # Pagination - 6 posts per page
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/home.html', {
        'page_obj': page_obj,
        'categories': categories,
    })


def post_detail_view(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')
    comments = post.comments.all().order_by('-created_at')
    related_posts = Post.objects.filter(
        category=post.category, status='published'
    ).exclude(id=post.id)[:3]

    # Check if user liked this post
    is_liked = False
    if request.user.is_authenticated:
        is_liked = Like.objects.filter(post=post, user=request.user).exists()

    # Handle comment form
    comment_form = CommentForm()
    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added!')
            return redirect('post_detail', slug=slug)

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'related_posts': related_posts,
        'is_liked': is_liked,
    })


@login_required
def post_create_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()  # saves tags
            messages.success(request, 'Post created!')
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form, 'action': 'Create'})


@login_required
def post_edit_view(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.author != request.user:
        messages.error(request, 'You can only edit your own posts.')
        return redirect('post_detail', slug=slug)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated!')
            return redirect('post_detail', slug=slug)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form, 'action': 'Edit'})


@login_required
def post_delete_view(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.author != request.user:
        messages.error(request, 'You can only delete your own posts.')
        return redirect('post_detail', slug=slug)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted!')
        return redirect('home')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})


@login_required
def like_post_view(request, slug):
    post = get_object_or_404(Post, slug=slug)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()  # unlike if already liked
    return redirect('post_detail', slug=slug)

def category_view(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category, status='published').order_by('-created_at')
    categories = Category.objects.all()
    context = {
        'category': category,
        'posts': posts,
        'categories': categories,
    }
    return render(request, 'blog/category.html', context)


def search_view(request):
    query = request.GET.get('q', '')
    posts = Post.objects.filter(
        Q(title__icontains=query) | Q(content__icontains=query),
        status='published'
    ).order_by('-created_at') if query else Post.objects.none()
    return render(request, 'blog/search.html', {'posts': posts, 'query': query})


@login_required
def my_posts_view(request):
    posts = Post.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'blog/my_posts.html', {'posts': posts})


def about_view(request):
    return render(request, 'blog/about.html')