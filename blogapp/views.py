from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.template.defaultfilters import slugify
from django.core.paginator import Paginator

from .forms import RegisterForm, BlogForm, CommentForm

from .models import *

def home(request):
    blogs = Blog.objects.order_by('-created_at')

    paginator = Paginator(blogs, 2)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)

    context = {
        'blogs': page_obj,
    }
    return render(request, "blogapp/home.html", context)

def blog_detail(request, slug):
    blog = Blog.objects.get(slug=slug)
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if request.user.is_anonymous:
            return redirect('login_page')
        else:
            if form.is_valid():
                form1 = form.save(commit=False)
                form1.user = request.user
                form1.blog = blog
                form1.save()
                return redirect('blog_detail', blog.slug)

    blog.views += 1
    blog.save()

    context = {
        'blog': blog,
        'form': form,
    }
    return render(request, "blogapp/blog_detail.html", context)

def category_blog(request, slug):
    category = Category.objects.get(slug=slug)
    blogs = Blog.objects.filter(category=category)
    context = {
        'category': category,
        'blogs': blogs,
    }
    return render(request, "blogapp/home.html", context)

def tag_blog(request, slug):
    tag = Tag.objects.get(slug=slug)
    blogs = Blog.objects.filter(tags=tag)
    context = {
        'tag': tag,
        'blogs': blogs,
    }
    return render(request, "blogapp/home.html", context)

def category_list(request):
    return render(request, "blogapp/category_list.html")

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, "Username or password is wrong!!!")
            return redirect('login_page')
    return render(request, "blogapp/login.html")

def log_out(request):
    logout(request)
    return redirect('home')

def register(request):

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()

    context = {
        'form': form,
    }
    return render(request, "blogapp/register.html", context)

@login_required(login_url='login_page')
def add_blog(request):
    form = BlogForm()
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            form1 = form.save(commit=False)
            form1.user = request.user
            form1.slug = slugify(form1.title)
            form1.save()
            blog = Blog.objects.get(id=form1.id)
            tags_list = form.cleaned_data['tags']
            tags = list(tags_list.split(','))
            for tag in tags:
                tag, create = Tag.objects.get_or_create(name=tag.strip())
                blog.tags.add(tag)
            return redirect('home')
    context = {
        'form': form,
    }
    return render(request, "blogapp/add_blog.html", context)

@login_required(login_url='login_page')
def update_blog(request, slug):
    blog = Blog.objects.get(slug=slug)
    form = BlogForm(request.POST or None, instance=blog)
    tags1 = blog.tags.all()
    teglar =""
    for i in range(len(tags1)):
        if i != len(tags1)-1:
            teglar += f"{tags1[i].name}, "
        else:
            teglar += f"{tags1[i].name}"
    print('teglar =', teglar)
    if request.method == 'POST':
        if form.is_valid():
            form1 = form.save(commit=False)
            form1.slug = slugify(form1.title)
            form1.save()
            tags_list = form.cleaned_data['tags']
            tags = list(tags_list.split(','))
            for tag in tags:
                tag, create = Tag.objects.get_or_create(name=tag.strip())
                blog.tags.add(tag)
            return redirect('blog_detail', blog.slug)
    context = {
        'blog': blog,
        'form': form,
        'teglar': teglar,
    }
    return render(request, "blogapp/update_blog.html", context)


@login_required(login_url='login_page')
def delete_blog(request, slug):
    blog = Blog.objects.get(slug=slug)
    form = BlogForm(request.POST or None, instance=blog)
    tags1 = blog.tags.all()
    teglar = ""
    for i in range(len(tags1)):
        if i != len(tags1) - 1:
            teglar += f"{tags1[i].name}, "
        else:
            teglar += f"{tags1[i].name}"
    print('teglar =', teglar)
    blog = Blog.objects.get(slug=slug)
    if request.method == 'POST':
        blog.delete()
        return redirect('home')
    context = {
        'blog': blog,
        'form': form,
        'teglar': teglar
    }
    return render(request, "blogapp/delete_blog.html", context)