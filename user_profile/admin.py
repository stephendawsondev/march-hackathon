# profile/admin.py
from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Profile
from .models import WomenInTech, OS_Maintainer, Mentor


@admin.register(Profile)
class ProfileAdmin(ModelAdmin):
    list_display = ("user", "created_at", "updated_at")
    search_fields = ("user__username", "user__email")
    readonly_fields = ("created_at", "updated_at")


@admin.register(WomenInTech)
class WomenInTechAdmin(ModelAdmin):
    list_display = ("user", "created_at", "updated_at")
    search_fields = ("user__username",)


@admin.register(OS_Maintainer)
class OS_MaintainerAdmin(ModelAdmin):
    list_display = ("user", "github_username", "created_at", "updated_at")
    search_fields = ("user__username", "github_username")


@admin.register(Mentor)
class MentorAdmin(ModelAdmin):
    list_display = ("user", "created_at", "updated_at")
    search_fields = ("user__username",)
