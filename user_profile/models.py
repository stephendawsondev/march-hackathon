from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    image = CloudinaryField("image", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse("profile_detail", kwargs={"username": self.user.username})

    def __str__(self):
        return f"{self.user.username}'s profile"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        Profile.objects.create(user=instance)


class WomenInTech(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    image = CloudinaryField("image", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # role fields
    is_woman_in_tech = models.BooleanField(default=False)

    # skills fields
    tech_specialties = models.CharField(max_length=200, blank=True)
    years_of_experience = models.IntegerField(null=True, blank=True)

    # Maintainer fields
    github_username = models.CharField(max_length=100, blank=True)
    maintained_projects = models.ManyToManyField(
        Project, blank=True
    )  # Need to create project model
    favourite_projects = models.ManyToManyField(
        Project, through=FavouriteProject, related_name="favourited_by", blank=True
    )  # Need to create Favourite project model for WIT to favourite project they are interested in
    contribution_focus = models.ManyToManyField(
        Project, through=ContributionFocus, related_name="focused_by", blank=True
    )  # Need to create ContributionFocus model for WIT to display what they are currently working on

    def get_absolute_url(self):
        return reverse("profile_detail", kwargs={"username": self.user.username})

    def __str__(self):
        return f"{self.user.username}'s profile"
