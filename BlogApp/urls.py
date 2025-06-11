from django.urls import path
from . import views

urlpatterns = [
    path('dash/', views.dash, name='dashboard' ),
    path('profile/', views.profile, name='profile'),
    path('guest/profile/<int:profile_id>/', views.guest_profile, name='guest_profile'),
    path('blog/<int:blog_id>/', views.blog, name='blog'),
    path('blog_<str:nickname>/<int:blog_id>/', views.guest_blog, name='guest_blog' ),
    path('read_post/<str:blog_name>_<int:blog_id>/post_<int:post_id>/', views.post, name='post'),
    path('read_post/guest/<str:blog_name>_<int:blog_id>/post_<int:post_id>/', views.guest_post, name='guest_post'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('create_blog/', views.create_blog, name='create_blog'),
    path('edit_blog/<int:blog_id>/', views.edit_blog, name='edit_blog'),
    path('delete_blog/<int:blog_id>/', views.delete_blog, name='delete_blog'),
    path('create_post/blog_<int:blog_id>/', views.create_post, name='create_post'),
    path('edit_post/<int:blog>/<int:post_id>/', views.edit_post, name='edit_post'),
    path('delete_post/<int:blog>/<int:post_id>/', views.delete_post, name='delete_post'),
    path('search/', views.global_search, name='global_search'),


]