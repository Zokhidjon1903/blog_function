from django.urls import path

from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('blog/<slug:slug>/', blog_detail, name='blog_detail'),
    path('category/<slug:slug>/', category_blog, name='category_blog'),
    path('tag/<slug:slug>/', tag_blog, name='tag_blog'),
    path('categories/', category_list, name='category_list'),
    path('login/', login_page, name='login_page'),
    path('logout/', log_out, name='log_out'),
    path('register/', register, name='register'),
    path('add_blog/', add_blog, name='add_blog'),
    path('update/<slug:slug>', update_blog, name='update_blog'),
    path('delete/<slug:slug>', delete_blog, name='delete_blog'),
]