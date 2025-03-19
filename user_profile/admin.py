# profile/admin.py
from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
