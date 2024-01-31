from django import template
from blog.models import Post, Category, Comment
from django.utils import timezone
from taggit.models import Tag

register = template.Library()


@register.simple_tag(name='comments_count')
def function(post_id):
    return Comment.objects.filter(post=post_id, approved=True).count()

@register.inclusion_tag('blog/blog-tags.html')
def blog_all_tags():
    tags = Tag.objects.all()
    return {'tags': tags}
    

@register.inclusion_tag('blog/blog-popular-posts.html')
def popular_posts(count=3, loggedin=False):
    posts = Post.objects.filter(status=1, published_date__lte=timezone.now()).order_by('-counted_views')[:count]
    return {'posts': posts, 'loggedin': loggedin}

@register.inclusion_tag('blog/blog-categories.html')
def categories_count():
    posts = Post.objects.filter(status=1, published_date__lte=timezone.now())
    categories = Category.objects.all()
    cats_dict = {}
    for name in categories:
        cats_dict[name] = posts.filter(category=name).count()
    return {'categories_count':cats_dict}
