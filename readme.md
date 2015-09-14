# Perforce project access portal

This portal makes it easy for people to manage multiple private projects within a Perforce server.
It allows certain people to define new project areas, and add/remove members through a simple web interface.

## Development

### One-time setup

#### Perforce

Install the Helix Versioning Engine (P4D), Visual Client (P4V), Command-Line (P4) and Helix Administration Tool (P4Admin) from http://www.perforce.com/downloads/helix .

Using P4Admin, in the "Users & Groups" tab, ensure there is a user named 'kalms'. Then, in the "Permissions" tab, ensure that there is a row that gives the user 'kalms' super-level access to all depots.

#### OpenLDAP

Install OpenLDAP for Windows from http://www.userbooster.de/en/download/openldap-for-windows.aspx .

Open c:\Program Files\OpenLDAP\slapd.conf and ensure that the following two lines are set appropriately:

suffix		"dc=example,dc=com"

rootdn		"cn=Manager,dc=example,dc=com"

After changing the config file, restart the OpenLDAP service using the "Services" manager in Windows.

Ensure that c:\Program Files\OpenLDAP\Client Tools is in your path.

#### Python

Install the latest Python 2.7.x from https://www.python.org/downloads/windows/

Install virtualenv: `c:\python27\scripts\pip install virtualenv`

Create a virtualenv: In the repository root directory, `virtualenv env` [docs](https://virtualenv.pypa.io/en/latest/userguide.html)

#### Populate LDAP

Open a command prompt.

Activate virtualenv: In the repository root directory, `env\scripts\activate` [docs](https://virtualenv.pypa.io/en/latest/userguide.html)

In the tests/ldap directory, `import_data.bat`

#### Populate Perforce

Using P4Admin, manually create a few P4 users which match 'uid' entries that are mentioned in the tests/ldap/example1.ldif file.

### Daily workflow

Open a command prompt.

Get latest from GitHub.

Activate virtualenv: In the repository root directory, `env\scripts\activate` [docs](https://virtualenv.pypa.io/en/latest/userguide.html)

Install dependent Python packages: `pip install -r requirements.txt` [docs](https://pip.pypa.io/en/latest/user_guide.html#requirements-files)

Ensure Django database is up-to-date: `python manage.py migrate` [docs](https://docs.djangoproject.com/en/1.8/topics/migrations/)

Update the list of new users from LDAP into the Django project: `python manage.py ldap_import`

Start the webservice: `python manage.py runserver` [docs](https://docs.djangoproject.com/en/1.8/ref/django-admin/)

To see the site, visit the URL `localhost:8000/projectaccess/` in your browser.
