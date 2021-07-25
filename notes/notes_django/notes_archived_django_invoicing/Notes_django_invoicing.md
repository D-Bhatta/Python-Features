# Notes on Django-Invoicing

Notes and code about Django-Invoicing.

## Sections

- [Notes on Django-Invoicing](#notes-on-django-invoicing)
  - [Sections](#sections)
  - [Notes](#notes)
  - [Setup the project](#setup-the-project)
    - [Create `homepage` view](#create-homepage-view)
      - [Create templates: `base.html`, `dummy.html`, `homepage.html`](#create-templates-basehtml-dummyhtml-homepagehtml)
      - [Create static assets](#create-static-assets)
      - [Create `homepage` view](#create-homepage-view-1)
    - [Configure tests](#configure-tests)
    - [Create tests](#create-tests)
    - [Prep remote and local databases](#prep-remote-and-local-databases)
    - [Integrate PostgreSQL in settings](#integrate-postgresql-in-settings)
  - [Add remote DB info to TravisCI config](#add-remote-db-info-to-travisci-config)
  - [Deploy Project](#deploy-project)
  - [Create a `Homepage`](#create-a-homepage)
    - [Main tasks](#main-tasks)
    - [Create a template: `homepage.html`](#create-a-template-homepagehtml)
    - [Add cards for each page](#add-cards-for-each-page)
    - [Add mock links to each card](#add-mock-links-to-each-card)
    - [Refactor links into real ones](#refactor-links-into-real-ones)
  - [Setup authentication](#setup-authentication)
    - [Main tasks](#main-tasks-1)
    - [Create an `users` app](#create-an-users-app)
    - [Add authentication urls](#add-authentication-urls)
  - [Add authentication templates](#add-authentication-templates)
  - [Refactor homepage to show user stuff only if logged in](#refactor-homepage-to-show-user-stuff-only-if-logged-in)
  - [Fix register](#fix-register)
  - [Email reset](#email-reset)
  - [Additional Information](#additional-information)
    - [Screenshots](#screenshots)
    - [Links](#links)
  - [Notes template](#notes-template)

## Notes

<!-- markdownlint-disable MD024 -->

## Setup the project

### Create `homepage` view

#### Create templates: `base.html`, `dummy.html`, `homepage.html`

- Create basic templates : `base.html`, `dummy.html`, `homepage.html`

```html
{% block header_content %} {% load static %}
<html>
  <meta charset="utf-8" />
  <meta
    name="viewport"
    content="width=device-width, initial-scale=1.0, user-scalable=yes"
  />
  <link rel="stylesheet" href="{% static 'css/ridge.css' %}" />
  <link rel="stylesheet" href="{% static 'css/ridge-light.css' %}" />
  <head>
    <title>Welcome to Invoicing!</title>
  </head>
  {% endblock header_content %}
</html>

```

```html
{% extends "base.html" %} {% load static %} {% block header_content %}
{{block.super }}
<body>
  <main>
    <vstack spacing="m">
      <vstack spacing="s" stretch="" align-x="center" align-y="center">
        <hstack responsive="" spacing="xl">
          <img
            src="{% static 'img/logo.png' %}"
            alt="logo"
            height="150"
            width="150"
          />
          <h1>Welcome to Invoicing!</h1>
        </hstack>
        <p><i>Your personal Invoicing app!</i></p>
        <p>
          Created by
          <a href="https://d-bhatta.github.io/Portfolio-Main/"
            >Debabrata Bhattacharya</a
          >
        </p>
      </vstack>
      <spacer></spacer>
      <vstack spacing="l">
        <vstack spacing="xs">
          <aside class="pa-s">
            <vstack> </vstack>
          </aside>
        </vstack>
      </vstack>
    </vstack>
  </main>
</body>
{% endblock header_content %}

```

```html
{% extends "base.html" %} {% load static %} {% block header_content %}
{{block.super }}
<head>
  <title>Welcome to Invoicing!</title>
</head>
<body>
  <main>
    <vstack spacing="s" stretch="" align-x="center" align-y="center">
      <h1>Welcome to Invoicing!</h1>
      <p>This is a dummy test page. It will have content shortly</p>
    </vstack>
  </main>
</body>
{% endblock header_content %}

```

#### Create static assets

- Create `static` folders and store assets
- We will be using light theme for this app
- Create a logo and store it in images

#### Create `homepage` view

- Create `homepage` view and render `homepage.html`

```python
def homepage(request):
    return render(request, "homepage.html", {})
```

- Create urls in `django_invoicing.urls`

```python
from django.urls import path

from django_invoicing import views

app_name = "invoicing"

urlpatterns = [path("home/", views.homepage, name="home")]
```

- Include in `django_apps.urls`

```python
"""django_apps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("invoicing/", include("django_invoicing.urls", namespace="invoicing")),
]
```

### Configure tests

- Create a `conftest.py` file
- Copy `base.html` to each `templates/` directory temporarily

```python
from os import remove
from shutil import copy, rmtree


def pytest_configure():
    copy(
        "django_invoicing/django_apps/templates/base.html",
        "django_invoicing/django_invoicing/templates/",
    )


def pytest_unconfigure():
    remove("django_invoicing/django_invoicing/templates/base.html")
```

### Create tests

- Create tests for the `home` view

```python
""" Tests for 'invoicing' app """
import pytest
from django.urls import reverse
from django_apps.utils import get_logger

lg = get_logger()

# This is supposed to fail
def test_helloworld():
    assert True == True


def test_view_homepage(client):
    url = reverse("invoicing:home")
    response = client.get(url)
    assert response.status_code == 200
```

### Prep remote and local databases

- Sign into pgAdmin for local and create a database
- Create a new role with access to the db
- Sign into local server with psql
- Create a new schema
- Create a table to test it out
- Sign into remote server with psql
- Create a new schema
- Create a table to test it out

### Integrate PostgreSQL in settings

- Add settings for connecting to a PostgreSQL backend in `settings.py`
- Test with ``env`` vars for local and remote DB servers

```python
try:
    DJANGO_ENVIRONMENT = os.environ["DJANGO_ENVIRONMENT"]
    DJANGO_HOST_NAME = os.environ["DJANGO_HOST_NAME"]
    DBNAME = os.environ["DBNAME"]
    DBUSER = os.environ["DBUSER"]
    DBPASSWORD = os.environ["DBPASSWORD"]
    DBHOST = os.environ["DBHOST"]
    DBPORT = os.environ["DBPORT"]

except KeyError:
    path_env = os.path.join(BASE_DIR.parent, ".env")
    dotenv.read_dotenv(path_env)
    DJANGO_ENVIRONMENT = os.environ["DJANGO_ENVIRONMENT"]
    DJANGO_HOST_NAME = os.environ["DJANGO_HOST_NAME"]
    DBNAME = os.environ["DBNAME"]
    DBUSER = os.environ["DBUSER"]
    DBPASSWORD = os.environ["DBPASSWORD"]
    DBHOST = os.environ["DBHOST"]
    DBPORT = os.environ["DBPORT"]
```

```python
#
# Settings for PostgreSQL
#
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": DBNAME,
        "USER": DBUSER,
        "PASSWORD": DBPASSWORD,
        "HOST": DBHOST,
        "PORT": DBPORT,
    }
}
```

## Add remote DB info to TravisCI config

- Install `travis` gem using    ```❯ gem install travis```
- Log into travis with ```❯ travis login --pro --github-token  token```
- Add the DB information using

    ```bash
    travis encrypt --pro DBNAME="name"  --add

    travis encrypt --pro DBUSER="user"  --add

    travis encrypt --pro DBPASSWORD="password"  --add

    travis encrypt --pro DBHOST="host"  --add

    travis encrypt --pro DBPORT="port"  --add

    ```

- There should be no space between the var name and the = and the value
- Push to TravisCI

## Deploy Project

- Create a `requirements.txt`. Heroku will use this file to install python dependencies, and recognise the project as a python project.

```requirements.txt
black==20.8b1
coveralls==2.1.2
cryptography==3.1.1
Django==3.1.2
django-dotenv==1.4.2
django-heroku==0.3.1
django-upload-validator==1.1.5
djangorestframework==3.12.1
Flask==1.1.2
grip==4.5.2
gunicorn==20.0.4
opencv-python==4.4.0.44
pip==20.2.4
pre-commit==2.7.1
psycopg2==2.8.6
pytest==6.1.1
pytest-cov==2.10.1
pytest-django==4.1.0
pytest-pythonpath==0.7.3
setuptools==50.3.2
social-auth-app-django==4.0.0
tox==3.20.1
twine==3.2.0
wheel==0.35.1
```

- Create a `Procfile` to deploy to Heroku. It will call the `gunicorn` server to start a worker for the app.
- Gunicorn requires a `pythopath` if the project files aren't in the same directory.

```Procfile
web: gunicorn --pythonpath django_invoicing django_apps.wsgi --log-file -

```

- Create a `runtime.txt`. It will tell Heroku what python runtime to use.

```txt
python-3.8.6
```

- Install `django-heroku`, `whitenoise` and `gunicorn`
- Install `heroku plugins:install heroku-repo` for resetting repos
- Install `heroku plugins:install heroku-config` for setting env vars
- Create the `static` files directory in the `BASE` directory with an `emptyfile.txt` file.
- Add them to requirements files in `requirements_dev.txt` and `requirements.txt`
- Add middleware and call `django_heroku.settings(locals())` in `settings.py`

```python
try:
    path_env = os.path.join(BASE_DIR.parent, ".env")
    dotenv.read_dotenv(path_env)
except (EnvironmentError, FileNotFoundError):  # Catch FileNotFoundError
    print("Couldn't retrieve the environment variables")

try:
    path_env = os.path.join(BASE_DIR.parent, ".env")
    dotenv.read_dotenv(path_env)  # Catch FileNotFoundError
    SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
except (KeyError, FileNotFoundError):
    path_env = os.path.join(BASE_DIR.parent, ".env")
    utils.generate_secret_key(path_env)
    dotenv.read_dotenv(path_env)
    SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
```

```python
if DJANGO_ENVIRONMENT == "PRODUCTION":
    ALLOWED_HOSTS = [DJANGO_HOST_NAME]
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "django_apps/static/django_apps"),
        # os.path.join(BASE_DIR, "django_invoicing/static/django_invoicing"),
    ]
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
elif DJANGO_ENVIRONMENT == "DEVELOPMENT":
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "django_apps\\static\\django_apps"),
        # os.path.join(BASE_DIR, "django_invoicing\\static\\django_invoicing"),
    ]
    ALLOWED_HOSTS = []
else:
    pass
```

```python
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Add whitenoise middleware
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "django_apps/templates/")
        ],  ## Add base templates directory
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]
```

```python
# Keep this at the end

if DJANGO_ENVIRONMENT == "PRODUCTION":
    django_heroku.settings(locals())
```

- Create heroku app with `heroku create d-djangoapps-1`
- Confirm that a remote named heroku has been set with `git remote -v`
- Set Env vars with `heroku config:push --file=env\r.env`
- Set `heroku config:set DEBUG_COLLECTSTATIC=1`
- Push code with `git push heroku setup:master`
- Check logs with `heroku logs --tail`

## Create a `Homepage`

### Main tasks

- Create a template: `homepage.html`
- Add cards for each page
- Add mock links to each card
- Refactor links into real ones

### Create a template: `homepage.html`

- Create template `homepage.html`
- Create a heading
- Add information about the app
- Move `head` tag at the top

```html
{% extends "base.html" %} {% load static %} {% block header_content %}
{{block.super }}
<head>
  <title>Welcome to Invoicing!</title>
</head>
<body>
  <main>
    <vstack spacing="m">
      <vstack spacing="s" stretch="" align-x="center" align-y="center">
        <hstack responsive="" spacing="xl">
          <img
            src="{% static 'img/logo.png' %}"
            alt="logo"
            height="150"
            width="150"
          />
          <h1>Welcome to Invoicing!</h1>
        </hstack>
        <p><i>Your personal Invoicing app!</i></p>
        <p>
          Created by
          <a href="https://d-bhatta.github.io/Portfolio-Main/"
            >Debabrata Bhattacharya</a
          >
        </p>
      </vstack>
      <spacer></spacer>
      <vstack spacing="s" stretch="" align-x="center" align-y="center">
        <h3>
          This app is made to function as a personal invoicing app for
          freelancers.
        </h3>
        <h3>This app promises the following:</h3>
        <ul>
          <li>The ability to generate invoices</li>
          <li>The ability to store invoice data as a set of fields</li>
          <li>The ability to log into the application</li>
          <li>The ability to generate PDF invoices</li>
          <li>The ability to retrieve invoices and view them</li>
        </ul>
      </vstack>
      <spacer></spacer>
      <vstack spacing="l">
        <vstack spacing="xs">
          <aside class="pa-s">
            <vstack> </vstack>
          </aside>
        </vstack>
      </vstack>
    </vstack>
  </main>
</body>
{% endblock header_content %}
<!-- homepage.html -->
```

```html
{% block header_content %} {% load static %}
<html>
  <meta charset="utf-8" />
  <meta
    name="viewport"
    content="width=device-width, initial-scale=1.0, user-scalable=yes"
  />
  <link rel="stylesheet" href="{% static 'css/ridge.css' %}" />
  <link rel="stylesheet" href="{% static 'css/ridge-light.css' %}" />
  {% endblock header_content %}
</html>
<!-- base.html -->
```

### Add cards for each page

- Create cards like in Nasa get in a flexible container

```html
<spacer></spacer>
<vstack spacing="l">
<vstack spacing="xs">
    <aside class="pa-l">
    <vstack>
        <section class="">
        <hstack
            responsive=""
            spacing="xl"
            class="bg-background-alt pa-m br-xs"
        >
            <aside stretch="" class="br-xs bn">
            <vstack>
                <a href="{% url 'invoicing:dummy' %}">
                <svg
                    class="br-xs br--top"
                    width="100%"
                    height="180"
                    xmlns="http://www.w3.org/2000/svg"
                    preserveAspectRatio="xMidYMid slice"
                    focusable="false"
                    role="img"
                    aria-label="Placeholder: Image cap"
                >
                    <title></title>
                    <rect
                    width="100%"
                    height="100%"
                    fill="#000000"
                    ></rect>
                    <image
                    href=" {% static 'img/logo.png' %}"
                    height="100%"
                    width="100%"
                    /></svg
                ></a>
                <hstack spacing="s" align-x="center">
                <h1>Name</h1>
                </hstack>
                <p class="pa-m">Description</p>
            </vstack>
            </aside>
            <aside stretch="" class="br-xs bn">
            <vstack>
                <a href="{% url 'invoicing:dummy' %}">
                <svg
                    class="br-xs br--top"
                    width="100%"
                    height="180"
                    xmlns="http://www.w3.org/2000/svg"
                    preserveAspectRatio="xMidYMid slice"
                    focusable="false"
                    role="img"
                    aria-label="Placeholder: Image cap"
                >
                    <title></title>
                    <rect
                    width="100%"
                    height="100%"
                    fill="#000000"
                    ></rect>
                    <image
                    href=" {% static 'img/logo.png' %}"
                    height="100%"
                    width="100%"
                    /></svg
                ></a>
                <hstack spacing="s" align-x="center">
                <h1>Name</h1>
                </hstack>
                <p class="pa-m">Description</p>
            </vstack>
            </aside>
        </hstack>
        <hstack
            responsive=""
            spacing="xl"
            class="bg-background-alt pa-m br-xs"
        >
            <aside stretch="" class="br-xs bn">
            <vstack>
                <a href="{% url 'invoicing:dummy' %}">
                <svg
                    class="br-xs br--top"
                    width="100%"
                    height="180"
                    xmlns="http://www.w3.org/2000/svg"
                    preserveAspectRatio="xMidYMid slice"
                    focusable="false"
                    role="img"
                    aria-label="Placeholder: Image cap"
                >
                    <title></title>
                    <rect
                    width="100%"
                    height="100%"
                    fill="#000000"
                    ></rect>
                    <image
                    href=" {% static 'img/logo.png' %}"
                    height="100%"
                    width="100%"
                    /></svg
                ></a>
                <hstack spacing="s" align-x="center">
                <h1>Name</h1>
                </hstack>
                <p class="pa-m">Description</p>
            </vstack>
            </aside>
            <aside stretch="" class="br-xs bn">
            <vstack>
                <a href="{% url 'invoicing:dummy' %}">
                <svg
                    class="br-xs br--top"
                    width="100%"
                    height="180"
                    xmlns="http://www.w3.org/2000/svg"
                    preserveAspectRatio="xMidYMid slice"
                    focusable="false"
                    role="img"
                    aria-label="Placeholder: Image cap"
                >
                    <title></title>
                    <rect
                    width="100%"
                    height="100%"
                    fill="#000000"
                    ></rect>
                    <image
                    href=" {% static 'img/logo.png' %}"
                    height="100%"
                    width="100%"
                    /></svg
                ></a>
                <hstack spacing="s" align-x="center">
                <h1>Name</h1>
                </hstack>
                <p class="pa-m">Description</p>
            </vstack>
            </aside>
        </hstack>
        </section>
    </vstack>
    </aside>
</vstack>
</vstack>
<spacer></spacer>
<vstack spacing="l">
<vstack spacing="xs">
    <aside class="pa-s">
    <vstack> </vstack>
    </aside>
</vstack>
</vstack>
```

### Add mock links to each card

- Add a url to the dummy template in a view

```python
from django.shortcuts import render
from django_apps.utils import get_logger

lg = get_logger()

# Create your views here.


def homepage(request):
    lg.debug("Rendering homepage")
    return render(request, "homepage.html", {})


def dummy(request):
    lg.debug("Rendering dummypage")
    return render(request, "dummy.html", {})
```

```python
urlpatterns = [
    path("home/", views.homepage, name="home"),
    path("dummy/", views.dummy, name="dummy"),
]
```

### Refactor links into real ones

- Refactor the links into real ones

## Setup authentication

- Setup authentication
- Show user stuff in homepage only if logged in

### Main tasks

- Create an `users` app
- Add authentication urls
- Add authentication templates
- Refactor homepage to show user stuff only if logged in

### Create an `users` app

- Create a users app with `python.exe manage.py startapp users`
- Disable password validators in settings. Just comment them out, leaving an empty list

```python
AUTH_PASSWORD_VALIDATORS = [
    # {
    #     "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    # },
    # {
    #     "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    # },
    # {
    #     "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    # },
    # {
    #     "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    # },
]
```

- Create a superuser with `python manage.py createsuperuser`
- In homepage display the current user's username and set a default with `{{ user.username | default:"Guest" }}`

```html
<vstack spacing="s" stretch="" align-x="center" align-y="center">
<hstack responsive="" spacing="xl">
    <img
    src="{% static 'img/logo.png' %}"
    alt="logo"
    height="150"
    width="150"
    />
    <h1>Welcome to Invoicing!</h1>
</hstack>
<p><i>Your personal Invoicing app!</i></p>
<p>
    Created by
    <a href="https://d-bhatta.github.io/Portfolio-Main/"
    >Debabrata Bhattacharya</a
    >
</p>
</vstack>
<hstack spacing="s" stretch="" align-x="center" align-y="center">
<h2>Hello {{ user.username | default:"Guest" }}!</h2>
</hstack>
```

### Add authentication urls

- Add the URLs provided by the Django authentication system into the app urls

```python
from django.urls import include, path
from users import views

urlpatterns = [path("accounts/", include("django.contrib.auth.urls"))]
```

```python
"""django_apps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("invoicing/", include("django_invoicing.urls", namespace="invoicing")),
    path("users/", include("users.urls")),
]
```

- Move the app to the top of the installed apps list

```python
INSTALLED_APPS = [
    "users",
    "django_invoicing",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
```

## Add authentication templates

- Create a login page `registration/login.html`

```html
{% extends "base.html" %} {% load static %} {% block header_content %}
{{block.super }}
<body>
  <main>
    <vstack spacing="m">
      <vstack spacing="s" stretch="" align-x="center" align-y="center">
        <hstack responsive="" spacing="xl">
          <img
            src="{% static 'img/logo.png' %}"
            alt="logo"
            height="150"
            width="150"
          />
          <h1>Welcome to Invoicing!</h1>
        </hstack>
        <p><i>Your personal Invoicing app!</i></p>
        <p>
          Created by
          <a href="https://d-bhatta.github.io/Portfolio-Main/"
            >Debabrata Bhattacharya</a
          >
        </p>
      </vstack>
      <hstack spacing="s" stretch="" align-x="center" align-y="center">
        <h2>Hello {{ user.username | default:"Guest" }}!</h2>
      </hstack>
      <spacer></spacer>
      {% if user.is_authenticated %}
      <vstack spacing="l">
        <vstack spacing="xs">
          <aside class="pa-s">
            <vstack spacing="s" stretch="" align-x="center" align-y="center">
              <h2>You are already logged in!</h2>
              <i><a href="{% url 'invoicing:home' %}">Back to home</a></i>
            </vstack>
          </aside>
        </vstack>
      </vstack>
      {% else %}
      <vstack spacing="l">
        <vstack spacing="xs">
          <aside class="pa-s">
            <vstack>
              <form method="POST">
                {% csrf_token %} {{form.as_p}}
                <button type="submit" value="login">LOGIN</button>
              </form>
              <a href="{% url 'invoicing:home' %}">Back to home</a>
            </vstack>
          </aside>
        </vstack>
      </vstack>
      {% endif %}
      <spacer></spacer>
      <vstack spacing="l">
        <vstack spacing="xs">
          <vstack spacing="s" stretch="" align-x="center" align-y="center">
            <h3>
              This app is made to function as a personal invoicing app for
              freelancers.
            </h3>
            <h3>This app promises the following:</h3>
            <ul>
              <li>The ability to generate invoices</li>
              <li>The ability to store invoice data as a set of fields</li>
              <li>The ability to log into the application</li>
              <li>The ability to generate PDF invoices</li>
              <li>The ability to retrieve invoices and view them</li>
            </ul>
          </vstack>
        </vstack>
      </vstack>
      <spacer></spacer>
      <vstack spacing="l">
        <vstack spacing="xs">
          <aside class="pa-s">
            <vstack> </vstack>
          </aside>
        </vstack>
      </vstack>
    </vstack>
  </main>
</body>
{% endblock header_content %}

```

- Redirect to `homepage` in settings

```python
LOGIN_REDIRECT_URL = "invoicing:home"
```

- Create test DB

```sql
CREATE DATABASE django_invoice_test
    WITH
    OWNER = main_user
    ENCODING = 'UTF8'
    LC_COLLATE = 'English_United States.1252'
    LC_CTYPE = 'English_United States.1252'
    TABLESPACE = pg_default
    CONNECTION LIMIT = 1000;

COMMENT ON DATABASE django_invoice_test
    IS 'Database for the Django-Invoice app';

GRANT TEMPORARY, CONNECT ON DATABASE django_invoice_test TO PUBLIC;

GRANT CREATE, CONNECT ON DATABASE django_invoice_test TO main_user;
GRANT TEMPORARY ON DATABASE django_invoice_test TO main_user WITH GRANT OPTION;
```

- Run and refactor, write tests, run and refactor

```python
""" Tests for 'users' app """
from os import environ

import pytest
from django.urls import reverse
from django_apps.utils import get_logger
from pytest_django.asserts import assertRedirects

from tests.fixtures import create_user

lg = get_logger()

# This is supposed to fail
def test_helloworld():
    assert True == True, "Basic tests failing"


def test_view_users_login_status(client):
    url = "/users/accounts/login/"
    response = client.get(url)
    assert response.status_code == 200, "Cant reach login page"


@pytest.mark.django_db
def test_users_login(client, create_user):
    USERNAME = environ["USERS_LOGIN_USERNAME"]
    PASSWORD = environ["USERS_LOGIN_PASSWORD"]
    response = client.login(username=USERNAME, password=PASSWORD)
    assert response == True, "Failed to login to app"

    url = reverse("invoicing:home")
    response = client.post(url)

    assert (
        response.context["user"].is_authenticated == True
    ), "Failed to verify authenticated status of user"
```

- Add logout and login links to `homepage`

```html
<hstack spacing="s" stretch="" align-x="center" align-y="center">
    <h2>Hello {{ user.username | default:"Guest" }}!</h2>
    <span
        >{% if user.is_authenticated %}
        <a href="{% url 'logout' %}"><button>Logout</button></a>
        {% else %}
        <a href="{% url 'login' %}"><button>Login</button></a>

        {% endif %}</span
    >
</hstack>
```

- Redirect logout to `homepage` in settings

```python
LOGOUT_REDIRECT_URL = "invoicing:home"
```

- Run and refactor, write tests, run and refactor

```python
@pytest.mark.django_db
def test_users_logout(client, create_user):
    USERNAME = environ["USERS_LOGIN_USERNAME"]
    PASSWORD = environ["USERS_LOGIN_PASSWORD"]

    # Log client in and check login
    client.login(username=USERNAME, password=PASSWORD)
    url = reverse("invoicing:home")
    response = client.post(url)
    login_status = response.context["user"].is_authenticated

    assert login_status == True, "Failed to login to app"

    # Check logout
    url = reverse("logout")
    response = client.get(url)
    with pytest.raises(TypeError):
        response.context["user"].is_authenticated

    # Check redirect
    assertRedirects(
        response=response,
        expected_url=reverse("invoicing:home"),
        status_code=302,
        msg_prefix="Failed to redirect to homepage aftre logout",
    )
```

- Create a Change Passwords Pages: `registration/password_change_done.html` and `registration/password_change_form.html`

```html
{% extends "base.html" %} {% load static %} {% block header_content %}
{{block.super }}
<body>
  <main>
    <vstack spacing="m">
      <vstack spacing="s" stretch="" align-x="center" align-y="center">
        <hstack responsive="" spacing="xl">
          <img
            src="{% static 'img/logo.png' %}"
            alt="logo"
            height="150"
            width="150"
          />
          <h1>Welcome to Invoicing!</h1>
        </hstack>
        <p><i>Your personal Invoicing app!</i></p>
        <p>
          Created by
          <a href="https://d-bhatta.github.io/Portfolio-Main/"
            >Debabrata Bhattacharya</a
          >
        </p>
      </vstack>
      <hstack spacing="s" stretch="" align-x="center" align-y="center">
        <h2>Hello {{ user.username | default:"Guest" }}!</h2>
        <h2>Change your password</h2>
      </hstack>
      <spacer></spacer>

      <vstack spacing="l">
        <vstack spacing="xs">
          <aside class="pa-s">
            <vstack>
              <form method="POST">
                {% csrf_token %} {{form.as_p}}
                <button type="submit" value="login">LOGIN</button>
              </form>
              <a href="{% url 'invoicing:home' %}">Back to home</a>
            </vstack>
          </aside>
        </vstack>
      </vstack>

      <spacer></spacer>
      <vstack spacing="l">
        <vstack spacing="xs">
          <vstack spacing="s" stretch="" align-x="center" align-y="center">
            <h3>
              This app is made to function as a personal invoicing app for
              freelancers.
            </h3>
            <h3>This app promises the following:</h3>
            <ul>
              <li>The ability to generate invoices</li>
              <li>The ability to store invoice data as a set of fields</li>
              <li>The ability to log into the application</li>
              <li>The ability to generate PDF invoices</li>
              <li>The ability to retrieve invoices and view them</li>
            </ul>
          </vstack>
        </vstack>
      </vstack>
      <spacer></spacer>
      <vstack spacing="l">
        <vstack spacing="xs">
          <aside class="pa-s">
            <vstack> </vstack>
          </aside>
        </vstack>
      </vstack>
    </vstack>
  </main>
</body>
{% endblock header_content %}

```

```html
{% extends "base.html" %} {% load static %} {% block header_content %}
{{block.super }}
<body>
  <main>
    <vstack spacing="m">
      <vstack spacing="s" stretch="" align-x="center" align-y="center">
        <hstack responsive="" spacing="xl">
          <img
            src="{% static 'img/logo.png' %}"
            alt="logo"
            height="150"
            width="150"
          />
          <h1>Welcome to Invoicing!</h1>
        </hstack>
        <p><i>Your personal Invoicing app!</i></p>
        <p>
          Created by
          <a href="https://d-bhatta.github.io/Portfolio-Main/"
            >Debabrata Bhattacharya</a
          >
        </p>
      </vstack>
      <hstack spacing="s" stretch="" align-x="center" align-y="center">
        <h2>Hello {{ user.username | default:"Guest" }}!</h2>
        <h2>Password has been successfully changed</h2>
      </hstack>
      <hstack spacing="s" stretch="" align-x="center" align-y="center">
        <a href="{% url 'invoicing:home' %}"><button>Home</button></a>
      </hstack>

      <spacer></spacer>

      <vstack spacing="l">
        <vstack spacing="xs">
          <vstack spacing="s" stretch="" align-x="center" align-y="center">
            <h3>
              This app is made to function as a personal invoicing app for
              freelancers.
            </h3>
            <h3>This app promises the following:</h3>
            <ul>
              <li>The ability to generate invoices</li>
              <li>The ability to store invoice data as a set of fields</li>
              <li>The ability to log into the application</li>
              <li>The ability to generate PDF invoices</li>
              <li>The ability to retrieve invoices and view them</li>
            </ul>
          </vstack>
        </vstack>
      </vstack>
      <spacer></spacer>
      <vstack spacing="l">
        <vstack spacing="xs">
          <aside class="pa-s">
            <vstack> </vstack>
          </aside>
        </vstack>
      </vstack>
    </vstack>
  </main>
</body>
{% endblock header_content %}

```

- Add a password change link to the `homepage`

```html
<hstack spacing="s" stretch="" align-x="center" align-y="center">
        <h2>Hello {{ user.username | default:"Guest" }}!</h2>
        <span
          >{% if user.is_authenticated %}
          <a href="{% url 'logout' %}"><button>Logout</button></a>
          <a href="{% url 'password_change' %}"
            ><button>Change Password</button></a
          >
          {% else %}
          <a href="{% url 'login' %}"><button>Login</button></a>

          {% endif %}</span
        >
      </hstack>
```

- Run and refactor, write tests, run and refactor

```python
@pytest.fixture
def logged_in(db, client, create_user):
    USERNAME = environ["USERS_LOGIN_USERNAME"]
    PASSWORD = environ["USERS_LOGIN_PASSWORD"]

    # Log client in and check login
    client.login(username=USERNAME, password=PASSWORD)

    return client
```

```python
@pytest.mark.django_db
def test_view_users_password_change_status(client, create_user, logged_in):
    url = reverse("password_change")
    response = client.get(url)
    assert response.status_code == 200, "Cant reach passowrd change page"


@pytest.mark.django_db
def test_view_users_password_change_done_status(client, create_user, logged_in):
    url = reverse("password_change_done")
    response = client.get(url)
    assert response.status_code == 200, "Cant reach passowrd change done page"
```

- Add email integration

```python
try:
    DJANGO_ENVIRONMENT = os.environ["DJANGO_ENVIRONMENT"]
    DJANGO_HOST_NAME = os.environ["DJANGO_HOST_NAME"]
    DBNAME = os.environ["DBNAME"]
    DBUSER = os.environ["DBUSER"]
    DBPASSWORD = os.environ["DBPASSWORD"]
    DBHOST = os.environ["DBHOST"]
    DBPORT = os.environ["DBPORT"]
    DBTEST = os.environ["DBTEST"]
    EMAIL_HOST = os.environ["EMAIL_HOST"]
    EMAIL_PORT = os.environ["EMAIL_PORT"]
    EMAIL_HOST_USER = os.environ["EMAIL_HOST_USER"]
    EMAIL_HOST_PASSWORD = os.environ["EMAIL_HOST_PASSWORD"]
    EMAIL_USE_TLS = os.environ["EMAIL_USE_TLS"]
    DEFAULT_FROM_EMAIL = os.environ["DEFAULT_FROM_EMAIL"]
    EMAIL_BACKEND = os.environ["EMAIL_BACKEND"]

except KeyError:
    path_env = os.path.join(BASE_DIR.parent, ".env")
    dotenv.read_dotenv(path_env)
    DJANGO_ENVIRONMENT = os.environ["DJANGO_ENVIRONMENT"]
    DJANGO_HOST_NAME = os.environ["DJANGO_HOST_NAME"]
    DBNAME = os.environ["DBNAME"]
    DBUSER = os.environ["DBUSER"]
    DBPASSWORD = os.environ["DBPASSWORD"]
    DBHOST = os.environ["DBHOST"]
    DBPORT = os.environ["DBPORT"]
    DBTEST = os.environ["DBTEST"]
    EMAIL_HOST = os.environ["EMAIL_HOST"]
    EMAIL_PORT = os.environ["EMAIL_PORT"]
    EMAIL_HOST_USER = os.environ["EMAIL_HOST_USER"]
    EMAIL_HOST_PASSWORD = os.environ["EMAIL_HOST_PASSWORD"]
    EMAIL_USE_TLS = os.environ["EMAIL_USE_TLS"]
    DEFAULT_FROM_EMAIL = os.environ["DEFAULT_FROM_EMAIL"]
    EMAIL_BACKEND = os.environ["EMAIL_BACKEND"]

if EMAIL_USE_TLS == "True":
    EMAIL_USE_TLS = True
if EMAIL_USE_TLS == "False":
    EMAIL_USE_TLS = False
```

- Run and refactor, write tests, run and refactor
- Create password reset templates

```html
{% extends "base.html" %} {% load static %} {% block header_content %}
{{block.super }}
<body>
  <main>
    <vstack spacing="m">
      <vstack spacing="s" stretch="" align-x="center" align-y="center">
        <hstack responsive="" spacing="xl">
          <img
            src="{% static 'img/logo.png' %}"
            alt="logo"
            height="150"
            width="150"
          />
          <h1>Welcome to Invoicing!</h1>
        </hstack>
        <p><i>Your personal Invoicing app!</i></p>
        <p>
          Created by
          <a href="https://d-bhatta.github.io/Portfolio-Main/"
            >Debabrata Bhattacharya</a
          >
        </p>
      </vstack>
      <hstack spacing="s" stretch="" align-x="center" align-y="center">
        <h2>Reset your password</h2>
      </hstack>
      <spacer></spacer>
      <vstack spacing="l">
        <vstack spacing="xs">
          <aside class="pa-s">
            <vstack>
              <form method="POST">
                {% csrf_token %} {{form.as_p}}
                <button type="submit" value="login">RESET</button>
              </form>
              <a href="{% url 'invoicing:home' %}">Back to home</a>
            </vstack>
          </aside>
        </vstack>
      </vstack>
      <spacer></spacer>
      <vstack spacing="l">
        <vstack spacing="xs">
          <vstack spacing="s" stretch="" align-x="center" align-y="center">
            <h3>
              This app is made to function as a personal invoicing app for
              freelancers.
            </h3>
            <h3>This app promises the following:</h3>
            <ul>
              <li>The ability to generate invoices</li>
              <li>The ability to store invoice data as a set of fields</li>
              <li>The ability to log into the application</li>
              <li>The ability to generate PDF invoices</li>
              <li>The ability to retrieve invoices and view them</li>
            </ul>
          </vstack>
        </vstack>
      </vstack>
      <spacer></spacer>
      <vstack spacing="l">
        <vstack spacing="xs">
          <aside class="pa-s">
            <vstack> </vstack>
          </aside>
        </vstack>
      </vstack>
    </vstack>
  </main>
</body>
{% endblock header_content %}

```

```html
{% extends "base.html" %} {% load static %} {% block header_content %}
{{block.super }}
<body>
  <main>
    <vstack spacing="m">
      <vstack spacing="s" stretch="" align-x="center" align-y="center">
        <hstack responsive="" spacing="xl">
          <img
            src="{% static 'img/logo.png' %}"
            alt="logo"
            height="150"
            width="150"
          />
          <h1>Welcome to Invoicing!</h1>
        </hstack>
        <p><i>Your personal Invoicing app!</i></p>
        <p>
          Created by
          <a href="https://d-bhatta.github.io/Portfolio-Main/"
            >Debabrata Bhattacharya</a
          >
        </p>
      </vstack>
      <hstack spacing="s" stretch="" align-x="center" align-y="center">
        <h2>Reset your password</h2>
      </hstack>
      <spacer></spacer>
      <vstack spacing="l">
        <vstack spacing="xs">
          <aside class="pa-s">
            <vstack>
              <form method="POST">
                {% csrf_token %} {{form.as_p}}
                <button type="submit" value="login">RESET</button>
              </form>
              <a href="{% url 'invoicing:home' %}">Back to home</a>
            </vstack>
          </aside>
        </vstack>
      </vstack>
      <spacer></spacer>
      <vstack spacing="l">
        <vstack spacing="xs">
          <vstack spacing="s" stretch="" align-x="center" align-y="center">
            <h3>
              This app is made to function as a personal invoicing app for
              freelancers.
            </h3>
            <h3>This app promises the following:</h3>
            <ul>
              <li>The ability to generate invoices</li>
              <li>The ability to store invoice data as a set of fields</li>
              <li>The ability to log into the application</li>
              <li>The ability to generate PDF invoices</li>
              <li>The ability to retrieve invoices and view them</li>
            </ul>
          </vstack>
        </vstack>
      </vstack>
      <spacer></spacer>
      <vstack spacing="l">
        <vstack spacing="xs">
          <aside class="pa-s">
            <vstack> </vstack>
          </aside>
        </vstack>
      </vstack>
    </vstack>
  </main>
</body>
{% endblock header_content %}

```

- Include a link to the password reset form on the login page

```html
<vstack spacing="l">
        <vstack spacing="xs">
          <aside class="pa-s">
            <vstack>
              <form method="POST">
                {% csrf_token %} {{form.as_p}}
                <button type="submit" value="login">LOGIN</button>
              </form>
              <a href="{% url 'invoicing:home' %}">Back to home</a>
              <a href="{% url 'password_reset' %}">Reset your password</a>
            </vstack>
          </aside>
        </vstack>
      </vstack>
```

- Run and refactor, write tests, run and refactor

```python
def test_view_users_password_reset_status(client):
    url = reverse("password_reset")
    response = client.get(url)
    assert response.status_code == 200, "Cant reach passowrd reset page"


def test_view_users_password_reset_done_status(client):
    url = reverse("password_reset_done")
    response = client.get(url)
    assert response.status_code == 200, "Cant reach passowrd reset done page"
```

- Add the email field by inheriting the `UserCreationForm` into `CustomUserCreationForm`  that extends Django’s `UserCreationForm`

```python
from django.contrib.auth.forms import UserCreationForm


class NewUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)
```

- Create a new view called `register`

```python
def register(request):
    lg.debug("Rendering register page")
    if request.method == "GET":
        return render(request, "register.html", {"form": NewUserCreationForm})
    elif request.method == "POST":
        form = NewUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("invoicing:home"))
```

- Add `register` url to `urls.py`

```python
urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/register/", views.register, name="register"),
]
```

- Create a template called `register.html`

```html
{% extends "base.html" %} {% load static %} {% block header_content %}
{{block.super }}
<body>
  <main>
    <vstack spacing="m">
      <vstack spacing="s" stretch="" align-x="center" align-y="center">
        <hstack responsive="" spacing="xl">
          <img
            src="{% static 'img/logo.png' %}"
            alt="logo"
            height="150"
            width="150"
          />
          <h1>Welcome to Invoicing!</h1>
        </hstack>
        <p><i>Your personal Invoicing app!</i></p>
        <p>
          Created by
          <a href="https://d-bhatta.github.io/Portfolio-Main/"
            >Debabrata Bhattacharya</a
          >
        </p>
      </vstack>
      <hstack spacing="s" stretch="" align-x="center" align-y="center">
        <h2>Hello {{ user.username | default:"Guest" }}!</h2>
      </hstack>
      <spacer></spacer>
      {% if user.is_authenticated %}
      <vstack spacing="l">
        <vstack spacing="xs">
          <aside class="pa-s">
            <vstack spacing="s" stretch="" align-x="center" align-y="center">
              <h2>You are already logged in!</h2>
              <i><a href="{% url 'invoicing:home' %}">Back to home</a></i>
            </vstack>
          </aside>
        </vstack>
      </vstack>
      {% else %}
      <vstack spacing="l">
        <vstack spacing="xs">
          <aside class="pa-s">
            <vstack>
              <form method="POST">
                {% csrf_token %} {{form.as_p}}
                <button type="submit" value="register">REGISTER</button>
              </form>
              <span
                ><a href="{% url 'login' %}"><button>Log into the app</button></a></span
              >
              <a href="{% url 'invoicing:home' %}">Back to home</a>
              <a href="{% url 'password_reset' %}">Reset your password</a>
            </vstack>
          </aside>
        </vstack>
      </vstack>
      {% endif %}
      <spacer></spacer>
      <vstack spacing="l">
        <vstack spacing="xs">
          <vstack spacing="s" stretch="" align-x="center" align-y="center">
            <h3>
              This app is made to function as a personal invoicing app for
              freelancers.
            </h3>
            <h3>This app promises the following:</h3>
            <ul>
              <li>The ability to generate invoices</li>
              <li>The ability to store invoice data as a set of fields</li>
              <li>The ability to log into the application</li>
              <li>The ability to generate PDF invoices</li>
              <li>The ability to retrieve invoices and view them</li>
            </ul>
          </vstack>
        </vstack>
      </vstack>
      <spacer></spacer>
      <vstack spacing="l">
        <vstack spacing="xs">
          <aside class="pa-s">
            <vstack> </vstack>
          </aside>
        </vstack>
      </vstack>
    </vstack>
  </main>
</body>
{% endblock header_content %}

```

- Add registration url to `login.html` template

```html
<vstack spacing="l">
    <vstack spacing="xs">
        <aside class="pa-s">
        <vstack>
            <form method="POST">
            {% csrf_token %} {{form.as_p}}
            <button type="submit" value="login">LOGIN</button>
            </form>
            <a href="{% url 'register' %}">Register your account</a>
            <a href="{% url 'invoicing:home' %}">Back to home</a>
            <a href="{% url 'password_reset' %}">Reset your password</a>
        </vstack>
        </aside>
    </vstack>
</vstack>
```

- Run and refactor, write tests, run and refactor

```python
@pytest.mark.parametrize(
    "username, password1, password2, email, validity",
    [
        ("John", "mary", "mary", "hello@example.com", True),
        ("John", "mary", "cat", "hello@example.com", False),
        ("", "mary", "mary", "hello@example.com", False),
        ("John", "", "mary", "hello@example.com", False),
        ("John", "mary", "", "hello@example.com", False),
    ],
)
def test_view_users_NewUserCreationForm(
    db, username, password1, password2, email, validity
):
    credentials = {
        "username": username,
        "password1": password1,
        "password2": password2,
        "email": email,
    }

    form = NewUserCreationForm(data=credentials)

    assert form.is_valid() == validity, "Invalid form: NewUserCreationForm".__add__(
        str(form.errors)
    )


def test_view_users_register_status(client):
    url = reverse("register")
    response = client.get(url)
    assert response.status_code == 200, "Cant reach registration page"


@pytest.mark.django_db
def test_view_users_register_post(client):
    credentials = {
        "username": "John",
        "password1": "johnpassword",
        "password2": "johnpassword",
        "email": "hello@example.com",
    }

    url = reverse("register")
    response = client.post(url, credentials)
    assert response.status_code == 302, "New user registration failed"
    assert response.url == reverse(
        "invoicing:home"
    ), "Didn't redirect to homepage after registration"
```

## Refactor homepage to show user stuff only if logged in

- Refactor homepage to hide stuff unless logged in

```html
      {% if user.is_authenticated %}
      <vstack spacing="l">
        <vstack spacing="s" stretch="" align-x="center" align-y="center">
          <h2>Your Dashboard</h2>
        </vstack>
        ...
      </vstack>
      <spacer></spacer>
      {% endif %}
```

- Run and refactor, write tests, run and refactor

```python
@pytest.mark.django_db
def test_reach_authenticated_only_content_home(client, create_user, logged_in):
    url = reverse("invoicing:home")
    response = client.get(url)
    assert (
        "Your Dashboard" in response.content.decode()
    ), "Cannot reach authenticated content"


def test_dont_reach_authenticated_only_content_home(client):
    url = reverse("invoicing:home")
    response = client.get(url)
    assert (
        "Your Dashboard" not in response.content.decode()
    ), "Authenticated content is reachable without authentication"
```

## Fix register

- Fix login button text on `register` page

```html
<vstack>
    <form method="POST">
    {% csrf_token %} {{form.as_p}}
    <button type="submit" value="register">REGISTER</button>
    </form>
    <span
    ><a href="{% url 'login' %}"><button>Login</button></a></span
    >
    <a href="{% url 'invoicing:home' %}">Back to home</a>
    <a href="{% url 'password_reset' %}">Reset your password</a>
</vstack>
```

## Email reset

- Test email reset manually
- Create template for password reset confirmation `password_reset_confirm.html`

```html
{% extends "base.html" %} {% load static %} {% block header_content %}
{{block.super }}
<body>
  <main>
    <vstack spacing="m">
      <vstack spacing="s" stretch="" align-x="center" align-y="center">
        <hstack responsive="" spacing="xl">
          <img
            src="{% static 'img/logo.png' %}"
            alt="logo"
            height="150"
            width="150"
          />
          <h1>Welcome to Invoicing!</h1>
        </hstack>
        <p><i>Your personal Invoicing app!</i></p>
        <p>
          Created by
          <a href="https://d-bhatta.github.io/Portfolio-Main/"
            >Debabrata Bhattacharya</a
          >
        </p>
      </vstack>
      <hstack spacing="s" stretch="" align-x="center" align-y="center">
        <h2>Change your password</h2>
      </hstack>
      <spacer></spacer>

      <vstack spacing="l">
        <vstack spacing="xs">
          <aside class="pa-s">
            <vstack>
              <form method="POST">
                {% csrf_token %} {{form.as_p}}
                <button type="submit" value="login">Change Passowrd</button>
              </form>
              <a href="{% url 'invoicing:home' %}">Back to home</a>
            </vstack>
          </aside>
        </vstack>
      </vstack>

      <spacer></spacer>
      <vstack spacing="l">
        <vstack spacing="xs">
          <vstack spacing="s" stretch="" align-x="center" align-y="center">
            <h3>
              This app is made to function as a personal invoicing app for
              freelancers.
            </h3>
            <h3>This app promises the following:</h3>
            <ul>
              <li>The ability to generate invoices</li>
              <li>The ability to store invoice data as a set of fields</li>
              <li>The ability to log into the application</li>
              <li>The ability to generate PDF invoices</li>
              <li>The ability to retrieve invoices and view them</li>
            </ul>
          </vstack>
        </vstack>
      </vstack>
      <spacer></spacer>
      <vstack spacing="l">
        <vstack spacing="xs">
          <aside class="pa-s">
            <vstack> </vstack>
          </aside>
        </vstack>
      </vstack>
    </vstack>
  </main>
</body>
{% endblock header_content %}

```

- Create template for password reset complete `password_reset_complete.html`

```html
{% extends "base.html" %} {% load static %} {% block header_content %}
{{block.super }}
<body>
  <main>
    <vstack spacing="m">
      <vstack spacing="s" stretch="" align-x="center" align-y="center">
        <hstack responsive="" spacing="xl">
          <img
            src="{% static 'img/logo.png' %}"
            alt="logo"
            height="150"
            width="150"
          />
          <h1>Welcome to Invoicing!</h1>
        </hstack>
        <p><i>Your personal Invoicing app!</i></p>
        <p>
          Created by
          <a href="https://d-bhatta.github.io/Portfolio-Main/"
            >Debabrata Bhattacharya</a
          >
        </p>
      </vstack>
      <hstack spacing="s" stretch="" align-x="center" align-y="center">
        <h2>Password has been successfully changed</h2>
      </hstack>
      <hstack spacing="s" stretch="" align-x="center" align-y="center">
        <a href="{% url 'invoicing:home' %}"><button>Home</button></a>
      </hstack>

      <spacer></spacer>

      <vstack spacing="l">
        <vstack spacing="xs">
          <vstack spacing="s" stretch="" align-x="center" align-y="center">
            <h3>
              This app is made to function as a personal invoicing app for
              freelancers.
            </h3>
            <h3>This app promises the following:</h3>
            <ul>
              <li>The ability to generate invoices</li>
              <li>The ability to store invoice data as a set of fields</li>
              <li>The ability to log into the application</li>
              <li>The ability to generate PDF invoices</li>
              <li>The ability to retrieve invoices and view them</li>
            </ul>
          </vstack>
        </vstack>
      </vstack>
      <spacer></spacer>
      <vstack spacing="l">
        <vstack spacing="xs">
          <aside class="pa-s">
            <vstack> </vstack>
          </aside>
        </vstack>
      </vstack>
    </vstack>
  </main>
</body>
{% endblock header_content %}

```



## Additional Information

### Screenshots

### Links

## Notes template

```python
```

```html

```
