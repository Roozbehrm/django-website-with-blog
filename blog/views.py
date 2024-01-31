from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post, Comment
from django.utils import timezone
from blog.forms import CommentForm_user, CommentForm_public
from django.contrib import messages
from django.core.paginator import (Paginator, EmptyPage, PageNotAnInteger )

# Create your views here.

def blog_view(request, **kwargs):
    posts = Post.objects.filter(status=1, published_date__lte=timezone.now())
    if catname := kwargs.get('cat_name'):
        #on host ssl return cat_name with %20 when it has space so we replace it with space
        catname = catname.replace('%20', ' ')
        posts = posts.filter(category__name= catname)
    if kwargs.get('username'):
        posts = posts.filter(author__username= kwargs.get('username'))
    if kwargs.get('tag_name'):
        posts = posts.filter(tags__name__in= [kwargs.get('tag_name')])
    posts = Paginator(posts, 3)
    try:
        page_number = request.GET.get('page')
        posts = posts.page(page_number)
    except PageNotAnInteger:
        posts = posts.get_page(1)
    except EmptyPage:
        posts = posts.get_page(1)
    context = {'posts': posts, 'catname': catname}
    return render(request, 'blog/blog-home.html', context)

def blog_single(request, pid):
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm_user(request.POST)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS, 'Comment submitted successfully and will publish after approval')
            else:
                messages.add_message(request, messages.ERROR, 'Comment could not send')
        else:
            form = CommentForm_public(request.POST)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS, 'Comment submitted successfully and will publish after approval')
            else:
                messages.add_message(request, messages.ERROR, 'Comment could not send')

    posts = Post.objects.filter(status=1, published_date__lte=timezone.now())
    post = get_object_or_404(posts, pk=pid)
    if not post.login_required or request.user.is_authenticated:
        comments = Comment.objects.filter(post = post.id, approved=True)
        next_post = posts.filter(id__gt=pid).order_by('id').first()
        prev_post = posts.filter(id__lt=pid).order_by('id').last()
        form = CommentForm_public()
        context = {'post': post, 'next_post': next_post, 'prev_post': prev_post, 'comments': comments, 'form': form}
        post.counted_views += 1
        post.save()
        return render(request, 'blog/blog-single.html', context)
    else:
        messages.add_message(request, messages.ERROR, 'You should be logged in to access this post')
        return redirect('/accounts/login')
    
def blog_search(request):
    posts = Post.objects.filter(status=1, published_date__lte=timezone.now())
    if  request.method == 'GET':
        if s := request.GET.get('s'):
                posts = posts.filter(content__icontains= s)
    context = {'posts': posts}
    return render(request, 'blog/blog-home.html', context)