# Perforce project access portal

This portal makes it easy for people to manage multiple private projects within a Perforce server.
It allows certain people to define new project areas, and add/remove members through a simple web interface.

## Development

### One-time setup

#### Perforce

Install the Helix Versioning Engine (P4D), Visual Client (P4V), Command-Line (P4) and Helix Administration Tool (P4Admin) from (http://www.perforce.com/downloads/helix)

#### Python

Install the latest Python 2.7.x from https://www.python.org/downloads/windows/

Install virtualenv: `c:\python27\scripts\pip install virtualenv`

Create a virtualenv: In the repository root directory, `virtualenv env` [docs](https://virtualenv.pypa.io/en/latest/userguide.html)

### Daily workflow

Activate virtualenv: In the repository root directory, `env\scripts\activate` [docs](https://virtualenv.pypa.io/en/latest/userguide.html)

Install dependent Python packages: `pip install -r requirements.txt` [docs](https://pip.pypa.io/en/latest/user_guide.html#requirements-files)

Ensure Django database is up-to-date: `python manage.py migrate` [docs](https://docs.djangoproject.com/en/1.8/topics/migrations/)

Start the webservice: `python manage.py runserver` [docs](https://docs.djangoproject.com/en/1.8/ref/django-admin/)

