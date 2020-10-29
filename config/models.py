from django.contrib import admin
from django.db import models


class Config(models.Model):
    key = models.CharField(max_length=255, unique=True)
    value = models.CharField(max_length=255, null=True, blank=True)


class ConfigAdmin(admin.ModelAdmin):
    list_display = ('key', 'value',)
