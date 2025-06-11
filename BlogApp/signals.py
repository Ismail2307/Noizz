from django.contrib.sites import requests
from django.core.files.base import ContentFile
from django.dispatch import receiver
from allauth.account.signals import user_logged_in, user_signed_up
from django.contrib.auth.models import User
from .models import Profile

@receiver(user_signed_up)
@receiver(user_logged_in)
def create_user_profile(request, user, **kwargs):
    profile, created = Profile.objects.get_or_create(user=user)

    if created:
        profile.nickname = user.username
        profile.save()


@receiver(user_signed_up)
def populate_profile_social(request, user, **kwargs):
    Profile.objects.get_or_create(user=user)
    sociallogin = kwargs.get('sociallogin')
    if sociallogin:
        data = sociallogin.account.extra_data
        profile = user.profile
        profile.bio = data.get('name', '')
        avatar_url = data.get('picture')
        if avatar_url:
            try:
                response = requests.get(avatar_url)
                if response.status_code == 200:
                    file_name = f"{user.username}_avatar.jpg"
                    profile.avatar.save(file_name, ContentFile(response.content), save=True)
            except:
                # fallback to default avatar
                profile.avatar.name = 'avatars/unknown.png'
                profile.save()
        else:
            profile.avatar.name = 'avatars/unknown.png'
            profile.save()
