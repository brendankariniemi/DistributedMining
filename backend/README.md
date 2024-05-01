# Getting Started with Django Backend

This project is the backend part of our application, developed using Django.

## Setting Up Your Development Environment

Before you can run this project, you'll need to set up your development environment. Here's how:

1. Ensure you have Python 3.8 or newer installed on your machine.
2. It's recommended to use a virtual environment for Python projects. Create one by running `python -m venv venv`.
3. Activate the virtual environment:
   - On Windows, run `venv\Scripts\activate`.
   - On macOS and Linux, run `source venv/bin/activate`.
4. Install the required dependencies by running `pip install -r requirements.txt`.

## Available Commands

In the project directory, you can run:

### `python manage.py runserver`

Starts the Django development server.\
Open [http://localhost:8000](http://localhost:8000) to view it in your browser.

The server will reload if you make edits.\
You will also see any lint errors in the console.

### `python manage.py test`

Runs the tests for the project. Django will automatically find tests you've written and run them.

### `python manage.py makemigrations` and `python manage.py migrate`

These commands generate and apply migrations, respectively, for your database models. Ensure you run these after making changes to your models to keep your database schema up to date.

### `python manage.py createsuperuser`

Creates a superuser account for the Django admin interface.

## Learn More

You can learn more about Django by visiting the [Django documentation](https://docs.djangoproject.com/en/3.2/).

### Django Admin

Django admin makes it easier to work with the data in your application. Once you've created a superuser account, visit [http://localhost:8000/admin](http://localhost:8000/admin) to access the admin interface.

### Django Rest Framework

This project uses Django Rest Framework for building APIs. You can learn more about it at [https://www.django-rest-framework.org/](https://www.django-rest-framework.org/).

### Deployment

Before deploying, ensure you've set `DEBUG` to `False` in your `settings.py` and configured your database properly for production.

Check out the Django deployment checklist at [https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/](https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/) for more information on deploying your Django project.

### Security

Django provides built-in protections against many security threats like SQL injection, cross-site scripting, and csrf attacks. Ensure you understand these protections and how to enable them in your project. The Django documentation provides extensive information on security.

---

We hope this guide helps you get started with your Django backend development!
