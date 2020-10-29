from django.contrib import admin

from author.models import Profile, ProfileAdmin

admin.site.register(Profile, ProfileAdmin)
