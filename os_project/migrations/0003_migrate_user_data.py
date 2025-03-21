from django.db import migrations
from django.contrib.auth.models import User


def link_existing_projects_to_profiles(apps, schema_editor):
    Project = apps.get_model("os_project", "Project")
    ProjectInterest = apps.get_model("os_project", "ProjectInterest")
    OS_Maintainer = apps.get_model("user_profile", "OS_Maintainer")
    WomenInTech = apps.get_model("user_profile", "WomenInTech")
    User = apps.get_model("auth", "User")

    # Update Project owners
    for project in Project.objects.filter(old_owner_id__isnull=False):
        try:
            user = User.objects.get(id=project.old_owner_id)
            osm = OS_Maintainer.objects.filter(user=user).first()
            if osm:
                project.owner = osm
                project.save(update_fields=["owner"])
        except User.DoesNotExist:
            continue

    # Update Project assigned WITs
    for project in Project.objects.filter(old_assigned_wit_id__isnull=False):
        try:
            user = User.objects.get(id=project.old_assigned_wit_id)
            wit = WomenInTech.objects.filter(user=user).first()
            if wit:
                project.assigned_wit = wit
                project.save(update_fields=["assigned_wit"])
        except User.DoesNotExist:
            continue

    # Update ProjectInterest WITs
    for interest in ProjectInterest.objects.filter(old_user_id__isnull=False):
        try:
            user = User.objects.get(id=interest.old_user_id)
            wit = WomenInTech.objects.filter(user=user).first()
            if wit:
                interest.wit = wit
                interest.save(update_fields=["wit"])
        except User.DoesNotExist:
            continue


def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        (
            "os_project",
            "0002_rename_assigned_wit_id_project_old_assigned_wit_id_and_more",
        ),
    ]

    operations = [
        migrations.RunPython(link_existing_projects_to_profiles, reverse_func),
    ]
