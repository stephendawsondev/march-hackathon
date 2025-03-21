from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile, WomenInTech, OS_Maintainer, Mentor


@receiver(post_save, sender=User)
def create_profiles_on_user_creation(sender, instance, created, **kwargs):
    if created:
        # Create the standard Profile for every user
        Profile.objects.create(user=instance)

        # Create specialized profiles based on user type
        user_type = getattr(instance, "_user_type", None)
        if user_type == "wit":
            WomenInTech.objects.create(user=instance, is_woman_in_tech=True)
        elif user_type == "osm":
            OS_Maintainer.objects.create(user=instance, is_os_maintainer=True)
        elif user_type == "mentor":
            Mentor.objects.create(user=instance)
