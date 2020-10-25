from django.contrib.auth.models import User
from django.db import models

from advert.helper import image_directory_path


class Profile(models.Model):
    avatar = models.ImageField(null=True, upload_to=image_directory_path)
    phone = models.CharField(max_length=64)
    facebook_id = models.CharField(max_length=64, null=True, blank=True)
    twitter_id = models.CharField(max_length=64, null=True, blank=True)
    youtube_id = models.CharField(max_length=64, null=True, blank=True)
    linkedin_id = models.CharField(max_length=64, null=True, blank=True)
    instagram_id = models.CharField(max_length=64, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
