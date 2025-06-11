from gc import get_objects

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import CreateBlogForm, EditProfileForm, CreatePostForm, CreatePostGGForm


@login_required()
def dash(request):
    blogs = Blog.objects.all().order_by('-created_at')
    return render(request, 'dashboard.html', {'blogs':blogs})


@login_required()
def profile(request):
    profile = request.user.profile
    blogs = Blog.objects.filter(owner = profile).order_by('-created_at')
    return render(request, 'profile_page.html', {'profile':profile, 'blogs':blogs})


@login_required()
def guest_profile(request, profile_id):
    profile = Profile.objects.get(id = profile_id)
    blogs = Blog.objects.filter(owner = profile).order_by('-created_at')
    return render(request, 'guest_profile.html', {'profile':profile, 'blogs':blogs})


@login_required()
def blog(request, blog_id):
    blog = Blog.objects.get(id = blog_id, owner=request.user.profile)
    posts = Post.objects.filter(blog = blog).order_by('-date')
    return render(request, 'blog.html', {'blog':blog, 'posts':posts})

@login_required()
def guest_blog(request, blog_id, nickname):
    profile = get_object_or_404(Profile, nickname = nickname )
    blog = Blog.objects.get(id=blog_id)
    posts = Post.objects.filter(blog=blog).order_by('-date')
    return render(request, 'guest_blog.html', {'blog': blog, 'posts': posts})


@login_required()
def post(request,blog_id, blog_name, post_id):
    blog = Blog.objects.get(id = blog_id, owner = request.user.profile, name = blog_name )
    post = Post.objects.get(blog = blog, id = post_id)
    return render(request, 'post.html', {'post':post, 'blog':blog} )

@login_required()
def guest_post(request,blog_id, blog_name, post_id):
    blog = Blog.objects.get(id = blog_id, name = blog_name )
    post = Post.objects.get(blog = blog, id = post_id)
    return render(request, 'guest_post.html', {'post':post, 'blog':blog} )




@login_required()
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = EditProfileForm(instance=profile)
    return render(request, 'edit_profile.html', {'profile':profile, 'form':form})


@login_required()
def create_blog(request):
    if request.method == 'POST':
        form = CreateBlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.owner = request.user.profile
            blog.save()
            return redirect('dashboard')
    else:
        form = CreateBlogForm()
    return render(request,'create_blog.html', {'form':form, 'heading':'Create Blog', 'button':'Create', 'is_edit':False})

@login_required()
def edit_blog(request, blog_id):
    blog = Blog.objects.get(id=blog_id, owner=request.user.profile)
    if request.method == 'POST':
        form = CreateBlogForm(request.POST, request.FILES, instance=blog )
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = CreateBlogForm(instance=blog)
    return render(request, 'create_blog.html', {'form':form, 'heading':'Edit Blog', 'button':'Save Changes', 'is_edit':True})


@login_required()
def delete_blog(request, blog_id):
    blog = Blog.objects.get(id=blog_id, owner=request.user.profile)
    if request.method == 'POST':
        blog.delete()
        return redirect('profile')
    return render(request, 'delete_blog.html', {'blog':blog})



# ############################################
@login_required()
def create_post(request, blog_id):
    blog = Blog.objects.get(id = blog_id, owner=request.user.profile)
    if request.method == 'POST':
        form = CreatePostGGForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            if blog:
                post.blog = blog
                post.save()
                return redirect('blog', blog_id=blog_id)

    else:
        form = CreatePostForm()
    return render(request, 'create_post.html', {'form':form, 'blog':blog})


@login_required()
def edit_post(request,blog, post_id):
    blog = Blog.objects.get(id = blog, owner=request.user.profile)
    post = Post.objects.get(id = post_id, blog=blog)
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog', blog.id)

    else:
        form = CreatePostForm( instance=post)
    return render(request, 'create_post.html', {'form':form, 'post':post, 'blog':blog})

@login_required()
def delete_post(request,blog, post_id):
    blog = Blog.objects.get(id  = blog, owner=request.user.profile)
    post = Post.objects.get(id = post_id, blog=blog)
    if request.method == 'POST':
        post.delete()
        return redirect('blog', blog.id)
    return render(request, 'delete_post.html', {'post':post, 'blog':blog})


def global_search(request):
    query = request.GET.get('q')
    search_type = request.GET.get('type')

    profiles = blogs = posts = []

    if query:
        if search_type == 'profiles':
            profiles = Profile.objects.filter(
                Q(nickname__icontains = query)
            )
        elif search_type == 'blogs':
            blogs = Blog.objects.filter(
                Q(name__icontains = query) |
                Q(description__icontains = query)

            )
        elif search_type == 'posts':
            posts = Post.objects.select_related('blog').filter(
                Q(title__icontains = query)|
                Q(content__icontains = query)
            )
    return render(request, 'search.html', {
            'query': query,
            'search_type': search_type,
            'profiles': profiles,
            'blogs': blogs,
            'posts': posts
        })

def custom_404(request, exception):
    return render(request, '404.html', status=404)

def custom_500(request):
    return render(request, '404.html', status=500)

def custom_403(request, exception):
    return render(request, '404.html', status=403)

def custom_400(request, exception):
    return render(request, '404.html', status=400)