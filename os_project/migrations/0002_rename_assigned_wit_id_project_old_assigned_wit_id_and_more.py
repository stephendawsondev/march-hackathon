from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("user_profile", "0003_mentor"),
        ("os_project", "0001_initial"),
    ]

    operations = [
        # First rename the fields to avoid conflicts
        migrations.RenameField(
            model_name="project",
            old_name="owner_id",
            new_name="old_owner_id",
        ),
        migrations.RenameField(
            model_name="project",
            old_name="assigned_wit_id",
            new_name="old_assigned_wit_id",
        ),
        migrations.RenameField(
            model_name="projectinterest",
            old_name="user_id",
            new_name="old_user_id",
        ),
        # Then add nullable fields
        migrations.AlterField(
            model_name="projectinterest",
            name="old_user_id",
            field=models.IntegerField(blank=True, null=True),
        ),
        # Add the new relationship fields
        migrations.AddField(
            model_name="project",
            name="owner",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="owned_projects",
                to="user_profile.os_maintainer",
            ),
        ),
        migrations.AddField(
            model_name="project",
            name="assigned_wit",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="assigned_projects",
                to="user_profile.womenintech",
            ),
        ),
        migrations.AddField(
            model_name="projectinterest",
            name="wit",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="project_interests",
                to="user_profile.womenintech",
            ),
        ),
        # Finally, update unique constraints
        migrations.AlterUniqueTogether(
            name="projectinterest",
            unique_together={("project", "wit")},
        ),
    ]
