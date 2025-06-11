from email.policy import default

from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE )
    nickname = models.CharField(max_length=255, default='User')
    bio = models.TextField(blank=True, default='The bio of User')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, default='avatars/unknown.png')

    def __str__(self):
        return self.nickname


class Blog(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True, default='blog_images/empty_blog.png')

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='post_images/', blank=True, null=True, default='post_images/empty_blog.png')
    date = models.DateTimeField(auto_now_add=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} - {self.date}"