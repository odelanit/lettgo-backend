from django.contrib import admin

from config.models import Config, ConfigAdmin

admin.site.register(Config, ConfigAdmin)
