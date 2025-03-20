from django.db import models
from cloudinary.models import CloudinaryField


class ProjectCategory(models.Model):
    """Categories for organizing projects"""

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Project categories"


class ProjectTag(models.Model):
    """Tags for filtering and organizing projects"""

    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    STATUS_CHOICES = [
        ("OPEN", "Open for Interest"),
        ("ASSIGNED", "WIT Assigned"),
        ("IN_PROGRESS", "In Progress"),
        ("COMPLETED", "Completed"),
    ]

    DIFFICULTY_CHOICES = [
        ("BEGINNER", "Beginner Friendly"),
        ("INTERMEDIATE", "Intermediate"),
        ("ADVANCED", "Advanced"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    repo_link = models.URLField()
    deploy_link = models.URLField(blank=True, null=True)
    image = CloudinaryField("image", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Placeholder fields - will be replaced with proper foreign keys later
    owner_id = models.IntegerField(null=True, blank=True)
    # TODO replace with when user_profile is finished:
    # owner = models.ForeignKey('user_profile.OSMProfile', on_delete=models.CASCADE, related_name='owned_projects')

    assigned_wit_id = models.IntegerField(null=True, blank=True)
    # TODO replace with when user_profile is finished:
    # assigned_wit = models.ForeignKey('user_profile.WITProfile', on_delete=models.SET_NULL,
    #                                  null=True, blank=True, related_name='assigned_projects')

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="OPEN")
    difficulty = models.CharField(
        max_length=15, choices=DIFFICULTY_CHOICES, default="INTERMEDIATE"
    )

    # Funding information
    funding_goal = models.DecimalField(max_digits=10, decimal_places=2)
    current_funding = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # TODO replace with when payments app is finished:
    # funding_goal = models.ForeignKey('payments.FundingGoal', on_delete=models.SET_NULL, null=True, related_name='project')
    # or keep as is and update the current_funding value based on payment records

    # Categories and tags
    category = models.ForeignKey(
        ProjectCategory, on_delete=models.SET_NULL, null=True, related_name="projects"
    )
    tags = models.ManyToManyField(ProjectTag, blank=True, related_name="projects")

    # For storing technologies used
    technologies = models.CharField(
        max_length=500, blank=True, help_text="Comma-separated list of technologies"
    )

    def __str__(self):
        return self.title

    def is_fully_funded(self):
        return self.current_funding >= self.funding_goal

    def funding_percentage(self):
        if self.funding_goal <= 0:
            return 0
        return min(100, int((self.current_funding / self.funding_goal) * 100))


class ProjectInterest(models.Model):
    """Track Women in Tech who are interested in a project"""

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="interested_users"
    )
    user_id = models.IntegerField()
    # TODO replace with when user_profile is finished:
    # wit = models.ForeignKey('user_profile.WITProfile', on_delete=models.CASCADE, related_name='project_interests')

    note = models.TextField(
        blank=True, help_text="Why are you interested in this project?"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("project", "user_id")
        # TODO replace with when user_profile is finished:
        # unique_together = ('project', 'wit')

    def __str__(self):
        return f"Interest in {self.project.title} (User: {self.user_id})"
        # TODO replace with when user_profile is finished:
        # return f"Interest in {self.project.title} by {self.wit.user.username}"
