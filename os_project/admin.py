from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Project, ProjectInterest, ProjectCategory, ProjectTag


@admin.register(ProjectCategory)
class ProjectCategoryAdmin(ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


@admin.register(ProjectTag)
class ProjectTagAdmin(ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


class ProjectInterestInline(admin.TabularInline):
    model = ProjectInterest
    extra = 0
    readonly_fields = ("created_at",)
    fields = ("user_id", "note", "created_at")
    # TODO: Update when user profiles are ready
    # fields = ('wit', 'note', 'created_at')


@admin.register(Project)
class ProjectAdmin(ModelAdmin):
    list_display = (
        "title",
        "status",
        "difficulty",
        "owner_id",
        "assigned_wit_id",
        "funding_goal",
        "current_funding",
        "is_fully_funded",
        "created_at",
    )
    list_filter = ("status", "difficulty", "category", "tags", "created_at")
    search_fields = ("title", "description", "technologies")
    readonly_fields = ("created_at", "updated_at")
    inlines = [ProjectInterestInline]

    fieldsets = (
        (
            "Basic Information",
            {"fields": ("title", "description", "image", "category", "tags")},
        ),
        (
            "Project Details",
            {
                "fields": (
                    "repo_link",
                    "deploy_link",
                    "technologies",
                    "difficulty",
                    "status",
                )
            },
        ),
        ("Funding Information", {"fields": ("funding_goal", "current_funding")}),
        (
            "Ownership",
            {
                "fields": ("owner_id", "assigned_wit_id")
                # TODO: Update when user profiles are ready
                # 'fields': ('owner', 'assigned_wit')
            },
        ),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    def is_fully_funded(self, obj):
        return obj.is_fully_funded()

    is_fully_funded.boolean = True
    is_fully_funded.short_description = "Fully Funded"


@admin.register(ProjectInterest)
class ProjectInterestAdmin(ModelAdmin):
    list_display = ("project", "user_id", "created_at")
    # TODO: Update when user profiles are ready
    # list_display = ('project', 'wit', 'created_at')
    list_filter = ("created_at",)
    search_fields = ("project__title", "note")
    readonly_fields = ("created_at",)
