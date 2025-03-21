from django.db import migrations


def populate_initial_data(apps, schema_editor):
    ProjectCategory = apps.get_model("os_project", "ProjectCategory")
    ProjectTag = apps.get_model("os_project", "ProjectTag")

    # Create categories
    categories = [
        {
            "name": "Library",
            "description": "Software libraries for various programming tasks",
        },
        {
            "name": "Framework",
            "description": "Application frameworks for building software",
        },
        {
            "name": "Compiler",
            "description": "Tools that translate code from one language to another",
        },
        {"name": "Web App", "description": "Applications that run in the browser"},
        {"name": "Mobile App", "description": "Applications for mobile devices"},
        {"name": "CLI Tool", "description": "Command-line interface tools"},
        {
            "name": "Other",
            "description": "Other types of projects not fitting into other categories",
        },
    ]

    for category_data in categories:
        ProjectCategory.objects.create(**category_data)

    # Create tags
    tags = [
        "Python",
        "JavaScript",
        "Java",
        "C#",
        "Ruby",
        "PHP",
        "TypeScript",
        "React",
        "Angular",
        "Vue",
        "Django",
        "Flask",
        "Rails",
        "Express",
        "Frontend",
        "Backend",
        "Fullstack",
        "API",
        "Database",
        "DevOps",
        "Machine Learning",
        "Data Science",
        "Blockchain",
        "Mobile",
        "Web",
        "Cloud",
        "Security",
        "Testing",
        "Documentation",
        "UI/UX",
        "Open Source",
        "Beginner Friendly",
        "Accessibility",
        "Internationalization",
    ]

    for tag_name in tags:
        ProjectTag.objects.create(name=tag_name)


def remove_initial_data(apps, schema_editor):
    # This is optional - delete initial data when migration is rolled back
    ProjectCategory = apps.get_model("os_project", "ProjectCategory")
    ProjectTag = apps.get_model("os_project", "ProjectTag")
    ProjectCategory.objects.all().delete()
    ProjectTag.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        (
            "os_project",
            "0001_initial",
        ),  # Make sure this matches your initial migration name
    ]

    operations = [
        migrations.RunPython(populate_initial_data, remove_initial_data),
    ]
