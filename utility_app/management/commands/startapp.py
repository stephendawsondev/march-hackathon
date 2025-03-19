import os
import re
import glob
from django.core.management.commands.startapp import Command as StartAppCommand


class Command(StartAppCommand):
    help = "Extends 'startapp' to use a custom template and replace placeholders."

    def handle(self, **options):
        app_name = options["name"]

        if not options.get("template"):
            options["template"] = "app_name"

        super().handle(**options)

        app_dir = os.path.join(os.getcwd(), app_name)

        # Get camel case version of app name for class names
        app_name_parts = app_name.split("_")
        app_name_camel_case = "".join(part.capitalize() for part in app_name_parts)

        # Update apps.py file
        with open(os.path.join(app_dir, "apps.py"), "r") as file:
            content = file.read()

        content = content.replace("MyAppConfig", f"{app_name_camel_case}Config")

        with open(os.path.join(app_dir, "apps.py"), "w") as file:
            file.write(content)

        # Update admin.py file to replace MyAppModel with CamelCaseAppNameModel
        admin_file = os.path.join(app_dir, "admin.py")
        if os.path.exists(admin_file):
            with open(admin_file, "r") as file:
                content = file.read()

            # Replace model and admin class names
            content = content.replace("MyAppModel", f"{app_name_camel_case}Model")
            content = content.replace("TheAppModel", f"{app_name_camel_case}Model")
            content = content.replace("TheAppAdmin", f"{app_name_camel_case}Admin")
            content = content.replace(
                "TheAppResource", f"{app_name_camel_case}Resource"
            )

            with open(admin_file, "w") as file:
                file.write(content)

        # Replace all instances of "app_name" with the actual app name
        self.replace_app_name_in_directory(app_dir, app_name)

        # Add the new app to INSTALLED_APPS in settings.py
        self.add_to_installed_apps(app_name)

    def replace_app_name_in_directory(self, directory, app_name):
        """
        Recursively replace 'app_name' with the actual app name in all files
        and directory names within the app.
        """
        # Rename directories containing "app_name"
        for root, dirs, files in os.walk(directory, topdown=False):
            # First handle files
            for file in files:
                filepath = os.path.join(root, file)
                # Skip __init__.py and other empty files
                if os.path.getsize(filepath) > 0:
                    self.replace_content_in_file(filepath, app_name)

                # Rename file if it contains "app_name"
                if "app_name" in file:
                    new_filename = file.replace("app_name", app_name)
                    new_filepath = os.path.join(root, new_filename)
                    os.rename(filepath, new_filepath)

            # Then handle directories
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)

                # Rename directory if it contains "app_name"
                if "app_name" in dir_name:
                    new_dir_name = dir_name.replace("app_name", app_name)
                    new_dir_path = os.path.join(root, new_dir_name)
                    if not os.path.exists(new_dir_path):
                        os.rename(dir_path, new_dir_path)

    def replace_content_in_file(self, filepath, app_name):
        """Replace 'app_name' with the actual app name in a file's content."""
        try:
            with open(filepath, "r") as file:
                content = file.read()

            # Replace "app_name" with the actual app name
            if "app_name" in content:
                modified_content = content.replace("app_name", app_name)

                with open(filepath, "w") as file:
                    file.write(modified_content)
        except UnicodeDecodeError:
            # Skip binary files
            pass

    def find_settings_file(self):
        """Find the Django settings.py file by searching the project."""
        # First try to get project name from manage.py
        project_name = None
        try:
            with open("manage.py", "r") as file:
                manage_content = file.read()
                match = re.search(
                    r"os\.environ\.setdefault\('DJANGO_SETTINGS_MODULE', '(.*?)\.settings'\)",
                    manage_content,
                )
                if match:
                    project_name = match.group(1)
                    settings_path = os.path.join(project_name, "settings.py")
                    if os.path.exists(settings_path):
                        return settings_path
        except Exception:
            pass

        # If we couldn't find it using manage.py, search for any settings.py file
        # Look in the root directory and immediate subdirectories
        settings_files = glob.glob("settings.py") + glob.glob("*/settings.py")

        # Filter out any that are in the 'venv' or similar directories
        settings_files = [
            f
            for f in settings_files
            if not any(
                exclude in f
                for exclude in ["venv", "env", ".env", ".venv", "__pycache__"]
            )
        ]

        if settings_files:
            # Return the first valid settings.py file
            return settings_files[0]

        return None

    def add_to_installed_apps(self, app_name):
        """Add the new app to INSTALLED_APPS in settings.py."""
        settings_path = self.find_settings_file()

        if not settings_path:
            self.stdout.write(
                self.style.ERROR(
                    "Could not find settings.py file. Please add the app manually to INSTALLED_APPS."
                )
            )
            return

        self.stdout.write(f"Found settings file at: {settings_path}")

        try:
            with open(settings_path, "r") as file:
                content = file.read()

            # Check if INSTALLED_APPS is in the content
            if "INSTALLED_APPS" not in content:
                self.stdout.write(
                    self.style.ERROR("Could not find INSTALLED_APPS in settings.py")
                )
                return

            # Find the installed apps list
            installed_apps_match = re.search(
                r"INSTALLED_APPS\s*=\s*\[(.*?)\]", content, re.DOTALL
            )

            if not installed_apps_match:
                self.stdout.write(
                    self.style.ERROR("Could not parse INSTALLED_APPS format")
                )
                return

            apps_content = installed_apps_match.group(1)

            # Check if the app is already in the list
            if f"'{app_name}'," in apps_content or f'"{app_name}",' in apps_content:
                self.stdout.write(
                    self.style.SUCCESS(f"App '{app_name}' is already in INSTALLED_APPS")
                )
                return

            # Find the last entry in the list
            lines = apps_content.split("\n")

            # Find the last non-empty line that contains an app entry
            last_app_line = None
            for i, line in enumerate(lines):
                stripped_line = line.strip()
                if (
                    stripped_line
                    and ("'" in stripped_line or '"' in stripped_line)
                    and "," in stripped_line
                    and not stripped_line.startswith("#")
                ):
                    last_app_line = i

            if last_app_line is not None:
                # Insert our new app after the last app
                lines_before = lines[: last_app_line + 1]
                lines_after = lines[last_app_line + 1 :]

                # Get the proper indentation level
                match = re.match(r"(\s*)", lines[last_app_line])
                indentation = match.group(1) if match else ""

                # Build new content
                new_lines = lines_before + [f"{indentation}'{app_name}',"] + lines_after
                new_apps_content = "\n".join(new_lines)

                # Replace the old INSTALLED_APPS content with new content
                new_content = content.replace(apps_content, new_apps_content)

                with open(settings_path, "w") as file:
                    file.write(new_content)

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully added '{app_name}' to INSTALLED_APPS"
                    )
                )
            else:
                self.stdout.write(
                    self.style.ERROR(
                        "Could not determine where to add the app in INSTALLED_APPS"
                    )
                )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Error updating INSTALLED_APPS: {str(e)}")
            )
