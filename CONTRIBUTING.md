# Contributing

Thank you for your interest in contributing to this Django template! This guide will help you set up your development environment and understand the workflow for making contributions.

## Development Environment Setup

### Option 1: Local Development

1. **Fork and clone the repository**

   Start by forking the repository on GitHub, then clone your fork:

   ```bash
   git clone https://github.com/your-username/django-auth-tw-template.git
   cd django-auth-tw-template
   ```

2. **Set up a virtual environment**

   On Windows:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

   On macOS/Linux:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install Python dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Install Node.js dependencies**

   ```bash
   npm install
   ```

5. **Create an environment file**

   Create a file named `env.py` in the project root directory with the following content:

   ```python
   import os

   os.environ["DATABASE_URL"] = "sqlite:///db.sqlite3"  # For development
   os.environ["SECRET_KEY"] = "your-development-secret-key"
   os.environ["CLOUDINARY_URL"] = "your-cloudinary-url"  # Optional for development
   os.environ["ALLOWED_HOSTS"] = "*"
   os.environ["CSRF_TRUSTED_ORIGINS"] = "http://* https://*"
   os.environ["DEBUG_MODE"] = "True"
   ```

### Option 2: Using Cloud IDE (Gitpod, CodeAnywhere, etc.)

If you're using a cloud IDE like Gitpod or CodeAnywhere, many of the setup steps are automated:

1. **Open the repository in your cloud IDE**
2. **Install Node.js dependencies**

   ```bash
   npm install
   ```

3. **Set up environment variables** according to your cloud IDE's documentation

## Running the Project

1. **Run database migrations**

   ```bash
   python manage.py migrate
   ```

2. **Start the Tailwind CSS compiler** in a separate terminal

   ```bash
   npm run dev
   ```

   This will watch for changes in your CSS files and automatically recompile them.

3. **Run the development server**

   ```bash
   python manage.py runserver
   ```

4. **Access the application** at <http://127.0.0.1:8000/> (or your cloud IDE's preview URL)

## Creating a New App

To create a new app using the template's custom app structure:

```bash
python manage.py startapp my_new_app
```

This command uses a custom template that:

- Sets up the proper directory structure
- Configures the app with the project's conventions
- Automatically adds the app to `INSTALLED_APPS` in settings.py

## Making Changes

1. **Create a new branch** for your feature or bugfix:

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** to the codebase

3. **Run tests** if applicable:

   ```bash
   python manage.py test
   ```

4. **Commit your changes** with a descriptive commit message:

   ```bash
   git add .
   git commit -m "Add feature: your feature description"
   ```

5. **Push to your fork**:

   ```bash
   git push origin feature/your-feature-name
   ```

6. **Open a pull request** against the main repository

## Coding Guidelines

- Follow PEP 8 style guide for Python code
- Write descriptive commit messages
- Include docstrings for new functions and classes
- Update documentation as needed

## Working with Tailwind CSS and DaisyUI

- When making CSS changes, make sure the Tailwind watcher is running (`npm run dev`)
- Use DaisyUI components when possible for consistency
- Custom CSS should be minimal and placed in the appropriate app's static directory
- For global styles, modify `src/styles/tailwind.css`

## Building for Production

Before deploying, build the CSS for production:

```bash
npm run build
```

This minifies the CSS output for better performance.
