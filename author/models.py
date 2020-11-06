from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
from django.utils.safestring import mark_safe

from advert.helper import image_directory_path


class Profile(models.Model):
    avatar = models.ImageField(null=True, upload_to=image_directory_path)
    phone = models.CharField(max_length=64, null=True, blank=True)
    facebook_id = models.CharField(max_length=64, null=True, blank=True)
    twitter_id = models.CharField(max_length=64, null=True, blank=True)
    youtube_id = models.CharField(max_length=64, null=True, blank=True)
    linkedin_id = models.CharField(max_length=64, null=True, blank=True)
    instagram_id = models.CharField(max_length=64, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    email_verified_at = models.DateTimeField(null=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    def avatar_tag(self):
        if self.avatar:
            return mark_safe('<img src="%s" style="width: 150px; height: 150px;" />' % self.avatar.url)
        else:
            return '-'
    avatar_tag.short_description = 'Avatar'


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'avatar_tag', 'phone', 'facebook_id', 'twitter_id', 'youtube_id', 'linkedin_id', 'instagram_id', 'website', 'email_verified_at',)
    readonly_fields = ('avatar_tag',)
