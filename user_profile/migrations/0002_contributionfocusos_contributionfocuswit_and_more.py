# Generated by Django 5.1.7 on 2025-03-21 09:28

import cloudinary.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("os_project", "0001_initial"),
        ("user_profile", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ContributionFocusOS",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("focus_area", models.CharField(max_length=100)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="os_project.project",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ContributionFocusWIT",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("focus_area", models.CharField(max_length=100)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="os_project.project",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="FavouriteProjectOS",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="os_project.project",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="FavouriteProjectWIT",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="os_project.project",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="OS_Maintainer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    cloudinary.models.CloudinaryField(
                        blank=True, max_length=255, null=True, verbose_name="image"
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_os_maintainer", models.BooleanField(default=False)),
                ("github_username", models.CharField(blank=True, max_length=100)),
                ("about", models.TextField(blank=True)),
                (
                    "contribution_focus",
                    models.ManyToManyField(
                        blank=True,
                        related_name="focused_by_os",
                        through="user_profile.ContributionFocusOS",
                        to="os_project.project",
                    ),
                ),
                (
                    "favourite_projects",
                    models.ManyToManyField(
                        blank=True,
                        related_name="favourited_by_os",
                        through="user_profile.FavouriteProjectOS",
                        to="os_project.project",
                    ),
                ),
                (
                    "maintained_projects",
                    models.ManyToManyField(blank=True, to="os_project.project"),
                ),
                (
                    "sponsored_projects",
                    models.ManyToManyField(
                        blank=True, related_name="sponsored_by", to="os_project.project"
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="os_maintainer_profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="favouriteprojectos",
            name="maintainer",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="user_profile.os_maintainer",
            ),
        ),
        migrations.AddField(
            model_name="contributionfocusos",
            name="maintainer",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="user_profile.os_maintainer",
            ),
        ),
        migrations.CreateModel(
            name="WomenInTech",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    cloudinary.models.CloudinaryField(
                        blank=True, max_length=255, null=True, verbose_name="image"
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_woman_in_tech", models.BooleanField(default=False)),
                ("tech_specialties", models.CharField(blank=True, max_length=200)),
                ("years_of_experience", models.IntegerField(blank=True, null=True)),
                ("github_username", models.CharField(blank=True, max_length=100)),
                ("about", models.TextField(blank=True)),
                (
                    "contribution_focus",
                    models.ManyToManyField(
                        blank=True,
                        related_name="focused_by_wit",
                        through="user_profile.ContributionFocusWIT",
                        to="os_project.project",
                    ),
                ),
                (
                    "favourite_projects",
                    models.ManyToManyField(
                        blank=True,
                        related_name="favourited_by_wit",
                        through="user_profile.FavouriteProjectWIT",
                        to="os_project.project",
                    ),
                ),
                (
                    "maintained_projects",
                    models.ManyToManyField(blank=True, to="os_project.project"),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="women_in_tech_profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="favouriteprojectwit",
            name="wit",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="user_profile.womenintech",
            ),
        ),
        migrations.AddField(
            model_name="contributionfocuswit",
            name="wit",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="user_profile.womenintech",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="favouriteprojectos",
            unique_together={("maintainer", "project")},
        ),
        migrations.AlterUniqueTogether(
            name="contributionfocusos",
            unique_together={("maintainer", "project")},
        ),
        migrations.AlterUniqueTogether(
            name="favouriteprojectwit",
            unique_together={("wit", "project")},
        ),
        migrations.AlterUniqueTogether(
            name="contributionfocuswit",
            unique_together={("wit", "project")},
        ),
    ]
