from django import forms
from .models import *

class CreateBlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['name', 'description', 'image']

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nickname', 'bio', 'avatar']

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'blog']

class CreatePostGGForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']