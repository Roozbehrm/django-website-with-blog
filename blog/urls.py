from django.urls import path
from blog.views import *


app_name ='blog'
urlpatterns = [
    path('', blog_view, name='index'),
    path('category/<str:cat_name>', blog_view, name='category'),
    path('author/<str:username>', blog_view, name='author'),
    path('search/', blog_search, name='search'),
    path('tag/<str:tag_name>', blog_view, name='tag'),
    path('<int:pid>', blog_single, name='single'),
]