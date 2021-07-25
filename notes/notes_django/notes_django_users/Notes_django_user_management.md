# Project_name

Notes and code about project_name

## Sections

- [Project_name](#project_name)
  - [Sections](#sections)
  - [Notes](#notes)
  - [Add PostgreSQL Integration](#add-postgresql-integration)
  - [Django User Management](#django-user-management)
    - [Create an app `django_users`](#create-an-app-django_users)
    - [Disable password validators in settings. Just comment them out, leaving an empty list](#disable-password-validators-in-settings-just-comment-them-out-leaving-an-empty-list)
    - [Create a superuser](#create-a-superuser)
  - [Create a Dashboard View](#create-a-dashboard-view)
  - [Work With Django User Management](#work-with-django-user-management)
    - [Create a login page](#create-a-login-page)
    - [Create a Logout Page](#create-a-logout-page)
    - [Change Passwords](#change-passwords)
    - [Send Password Reset Links](#send-password-reset-links)
      - [Change Email Templates](#change-email-templates)
  - [Register New Users](#register-new-users)
  - [Send Emails to the Outside World: Mail gun](#send-emails-to-the-outside-world-mail-gun)
  - [Log in With GitHub](#log-in-with-github)
    - [Select Authentication backend](#select-authentication-backend)
  - [Gmail SMTP](#gmail-smtp)
  - [Finalise](#finalise)
  - [Notes template](#notes-template)

## Notes

Notes about Django User Management.

## Add PostgreSQL Integration

1. Change settings to use PostgreSQL instead of SQLite
2. Install `travis` gem using    ```❯ gem install travis```

3. Log into travis with ```❯ travis login --pro --github-token  token```
4. Add the DB information using

    ```bash
    travis encrypt --pro DBNAME="name"  --add

    travis encrypt --pro DBUSER="user"  --add

    travis encrypt --pro DBPASSWORD="password"  --add

    travis encrypt --pro DBHOST="host"  --add

    travis encrypt --pro DBPORT="port"  --add

    ```

5. There should be no space between the var name and the = and the value
6. Push to TravisCI

## Django User Management

### Create an app `django_users`

```bash
> python.exe manage.py startapp django_users
```

### Disable password validators in settings. Just comment them out, leaving an empty list

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

### Create a superuser

```bash
python manage.py createsuperuser
```

## Create a Dashboard View

- Most user management systems have some sort of main page, usually known as a dashboard.
- Create a base template
- Create a `dashboard.html` file
- Display the current user's username and set a default with `{{ user.username | default:"Guest" }}`

```html
{% extends "base.html" %} {% load static %} {% block header_content %}
{{block.super }}
<body>
  <main>
    <vstack spacing="m">
      <vstack spacing="s" stretch="" align-x="center" align-y="center">
        <h1>Django-Users</h1>
        <h2>Hello {{ user.username | default:"Guest" }}!</h2>
      </vstack>
      <spacer></spacer>
      <vstack spacing="l">
        <vstack spacing="xs">
          <aside class="pa-s">
            <vstack>
            </vstack>
          </aside>
        </vstack>
      </vstack>
    </vstack>
  </main>
</body>
{% endblock header_content %}
```

- If the user isn’t logged in, then Django will still set the user variable using an `AnonymousUser` object. An anonymous user always has an empty username, so the dashboard will show `Hello, Guest!`
- Create a view to render it

```python
from django.shortcuts import render

# Create your views here.


def dashboard(request):
    return render(request, "dashboard.html", {})
```

- Set an url to access the view.
- Do not add a namespacefor this app.

```python
from django.urls import path

from django_users import views

urlpatterns = [path("dashboard/", views.dashboard, name="dashboard")]
```

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [path("admin/", admin.site.urls), path("", include("django_users.urls"))]
```

## Work With Django User Management

- Django has a lot of user management–related resources that’ll take care of almost everything, including login, logout, password change, and password reset. Templates aren’t part of those resources, though. You have to create them on your own.

- Add the URLs provided by the Django authentication system into the app urls

```python
urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("accounts/", include("django.contrib.auth.urls")),
]
```

- Move the app to the top of the installed apps list

```python
# Application definition

INSTALLED_APPS = [
    "django_users",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
```

### Create a login page

- For the login page, Django will try to use a template called `registration/login.html`

```html
{% extends "base.html" %} {% load static %} {% block header_content %}
{{block.super }}
<body>
  <main>
    <vstack spacing="m">
      <vstack spacing="s" stretch="" align-x="center" align-y="center">
        <h1>Django-Users: Login</h1>
        <h2>Hello {{user.username|default:"Guest"}}!</h2>
      </vstack>
      <spacer></spacer>
      <vstack spacing="l">
        <vstack spacing="xs">
          <aside class="pa-s">
            <vstack>
              <form method="POST">
                {% csrf_token %} {{form.as_p}}
                <input type="submit" value="login" />
              </form>
              <a href="{% url 'dashboard' %}">Back to dashboard</a>
            </vstack>
          </aside>
        </vstack>
      </vstack>
    </vstack>
  </main>
</body>
{% endblock header_content %}

```

- Django will automatically create the view and urls necessary for the template.
- Redirect to dashboard in settings

```python
LOGIN_REDIRECT_URL = "dashboard"
```

### Create a Logout Page

- Users can log in, but they should also be able to log out. This process is more straightforward because there’s no form—they just need to click a link. After that, Django will redirect users to `accounts/logout` and will try to use a template called `registration/logged_out.html`.
- Redirect them to the dashboard

```python
LOGOUT_REDIRECT_URL = "dashboard"
```

- Add logout and login links to dashboard

```html
<hstack spacing="s">
        <h2>Hello {{user.username|default:"Guest"}}!</h2>
        <span>
            {% if user.is_authenticated %}
            <a href="{% url 'logout' %}">Logout</a>
            {% else %}
            <a href="{% url 'login' %}">Login</a>
            {% endif %}
        </span>
        </hstack>
```

### Change Passwords

- Django needs two templates to make this work

1. `registration/password_change_form.html` to display the password change form
2. `registration/password_change_done.html` to show a confirmation that the password was successfully changed

- Create `registration/password_change_form.html`

```html
{% extends "base.html" %} {% load static %} {% block header_content %}
{{block.super }}
<body>
  <main>
    <vstack spacing="m">
      <vstack spacing="s" stretch="" align-x="center" align-y="center">
        <h1>Django-Users: Change Password</h1>
        <h2>Hello {{user.username|default:"Guest"}}!</h2>
      </vstack>
      <spacer></spacer>
      <vstack spacing="l">
        <vstack spacing="xs">
          <aside class="pa-s">
            <vstack>
              <form method="POST">
                {% csrf_token %} {{form.as_p}}
                <input type="submit" value="change" />
              </form>
              <a href="{% url 'dashboard' %}">Back to dashboard</a>
            </vstack>
          </aside>
        </vstack>
      </vstack>
    </vstack>
  </main>
</body>
{% endblock header_content %}

```

- This template looks almost the same as the login template you created earlier. But this time, Django will put a password change form here, not a login form, so the browser will display it differently.

- Create `registration/password_change_done.html`:

```html
{% extends "base.html" %} {% load static %} {% block header_content %}
{{block.super }}
<body>
  <main>
    <vstack spacing="m">
      <vstack spacing="s" stretch="" align-x="center" align-y="center">
        <h1>Django-Users: Password has been successfully changed</h1>
        <h2>Hello {{user.username|default:"Guest"}}!</h2>
      </vstack>
      <spacer></spacer>
    </vstack>
  </main>
</body>
{% endblock header_content %}

```

- This will reassure users that the password change was successful and let them go back to the dashboard.
- Add a password change link to the dashboard

```html
            {% if user.is_authenticated %}
            <a href="{% url 'logout' %}">Logout</a>
            <a href="{% url 'password_change' %}"> Change Password</a>
```

### Send Password Reset Links

- In `settings.py` add the following

```python
EMAIL_HOST = "host"

EMAIL_PORT = "port_number"

EMAIL_USE_TLS = False or True  # Depending on smtp server

DEFAULT_FROM_EMAIL = "example@example.com"
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
SERVER_EMAIL = "example@example.com"
```

- Run this command in the terminal

```bash
python -m smtpd -d -n -c DebuggingServer "host":"port_number"
```

- This will start a simple SMTP server. It won’t send any emails to actual email addresses. Instead, it’ll show the content of the messages in the command line.
- `smtpd` is deprecated, so it is better to use: `python -m aiosmtpd -d -n -l 127.0.0.1:1025`
- Add a `registration/password_reset_form.html` to display the form used to request a password reset email

```html
{% extends "base.html" %} {% load static %} {% block header_content %}
{{block.super }}
<body>
  <main>
    <vstack spacing="m">
      <vstack spacing="s" stretch="" align-x="center" align-y="center">
        <h1>Django-Users: Send Password reset link in email</h1>
        <h2>Hello {{user.username|default:"Guest"}}!</h2>
      </vstack>
      <spacer></spacer>
      <vstack spacing="l">
        <vstack spacing="xs">
          <aside class="pa-s">
            <vstack>
              <form method="POST">
                {% csrf_token %} {{form.as_p}}
                <input type="submit" value="change" />
              </form>
              <a href="{% url 'dashboard' %}">Back to dashboard</a>
            </vstack>
          </aside>
        </vstack>
      </vstack>
    </vstack>
  </main>
</body>
{% endblock header_content %}

```

- Add a `registration/password_reset_done.html` to show a confirmation that a password reset email was sent

```html
{% extends "base.html" %} {% load static %} {% block header_content %}
{{block.super }}
<body>
  <main>
    <vstack spacing="m">
      <vstack spacing="s" stretch="" align-x="center" align-y="center">
        <h1>Django-Users: Password reset done</h1>
        <h2>Hello {{user.username|default:"Guest"}}!</h2>
      </vstack>
      <spacer></spacer>
      <a href="{% url 'login' %}">Back to dashboard</a>
    </vstack>
  </main>
</body>
{% endblock header_content %}

```

- Include a link to the password reset form on the login page

```html
<vstack>
    <form method="POST">
    {% csrf_token %} {{form.as_p}}
    <input type="submit" value="login" />
    </form>
    <a href="{% url 'dashboard' %}">Back to dashboard</a>
    <a href="{% url 'password_reset' %}">Back to dashboard</a>
</vstack>
```

- The email should print to the terminal from the `smtpd`/`aiosmtpd` server

#### Change Email Templates

- `registration/password_reset_email.html` determines the body of the email
- `registration/password_reset_subject.txt` determines the subject of the email

```html
Password reset for email {{ email }}. Follow the link below: {{ protocol}}://{{
domain }}{% url 'password_reset_confirm' uidb64=uid token=token %}

```

```txt
Password reset for Django-Users
```

## Register New Users

- Django doesn’t provide user registration out of the box.
- `UserCreationForm`: It contains all the necessary fields to create a new user
- However, it doesn’t include an email field.
- Add the email field by inheriting the `UserCreationForm` into a new form
- `CustomUserCreationForm` extends Django’s `UserCreationForm`. The inner class `Meta` keeps additional information about the form and in this case extends `UserCreationForm.Meta`, so almost everything from Django’s form will be reused.
- The key difference is the `fields` attribute, which determines the fields that’ll be included in the form. Your custom form will use all the fields from `UserCreationForm` and will add the `email` field.

```python
from django.contrib.auth.forms import UserCreationForm


class NewUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)
```

- Create a new view called `register`

```python
def register(request):
    if request.method == "GET":
        return render(request, "register.html", {"form": NewUserCreationForm})
    elif request.method == "POST":
        form = NewUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("dashboard"))
```

- Add `register` url to `urls.py`

```python
path("register/", views.register, name="register"),
```

- Create a template called `register.html`

```html
{% extends "base.html" %} {% load static %} {% block header_content %}
{{block.super }}
<body>
  <main>
    <vstack spacing="m">
      <vstack spacing="s" stretch="" align-x="center" align-y="center">
        <h1>Django-Users: Register</h1>
      </vstack>
      <spacer></spacer>
      <vstack spacing="l">
        <vstack spacing="xs">
          <aside class="pa-s">
            <vstack>
              <form method="POST">
                {% csrf_token %} {{form.as_p}}
                <input type="submit" value="register" />
              </form>
              <a href="{% url 'login' %}">Login</a>
            </vstack>
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
<vstack>
    <form method="POST">
    {% csrf_token %} {{form.as_p}}
    <input type="submit" value="login" />
    </form>
    <a href="{% url 'dashboard' %}">Back to dashboard</a>
    <a href="{% url 'password_reset' %}">Back to dashboard</a>
    <a href="{% url 'register' %}">Register</a>
</vstack>
```

## Send Emails to the Outside World: Mail gun

- Create a mailgun account
- Go to Dashboard -> domain -> select SMTP
- Copy credentials that appear

```env
EMAIL_HOST = smtp.mailgun.org

EMAIL_HOST_USER = Username

EMAIL_HOST_PASSWORD = password

EMAIL_PORT = 587

EMAIL_USE_TLS = True

EMAIL_BACKEND = django.core.mail.backends.smtp.EmailBackend

DEFAULT_FROM_EMAIL = Username
```

- Now, email should be sent from mailgun everytime.

## Log in With GitHub

- Install social auth with `pip install social-auth-app-django`
- Add it to `INSTALLED_APPS`

```python
INSTALLED_APPS = ["django_users", "social_django", """..."""]
```

- Add two context processors to settings.py

```python
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["django_apps/templates/"],  ## Add base templates directory
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                """...""" "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",
            ]
        },
    }
]
```

- Apply the migrations

```bash
❯ python.exe .\manage.py makemigrations
```

```bash
❯ python.exe .\manage.py migrate
```

- Include the social authentication URLs in your app

```python
path("oauth/", include("social_django.urls")),
```

- To use social authentication specifically with GitHub, you have to add a dedicated authentication backend.

```python
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "social_core.backends.github.GithubOAuth2",
]
```

- Add a link to the GitHub login on your login page

```html
<a href="{% url 'social:begin' 'github' %}">Login with Github</a>
```

- Go to [GitHub’s page for registering a new OAuth application](https://github.com/settings/applications/new)
- The most important part is the **Authorization Callback URL**. It has to point back to your application.
- Add the values of `Client ID` and `Client Secret` to settings as `SOCIAL_AUTH_GITHUB_KEY`  and `SOCIAL_AUTH_GITHUB_SECRET`

```python
try:
    """..."""
    SOCIAL_AUTH_GITHUB_KEY = os.environ["SOCIAL_AUTH_GITHUB_KEY"]
    SOCIAL_AUTH_GITHUB_SECRET = os.environ["SOCIAL_AUTH_GITHUB_SECRET"]
except KeyError:
    """..."""
    SOCIAL_AUTH_GITHUB_KEY = os.environ["SOCIAL_AUTH_GITHUB_KEY"]
    SOCIAL_AUTH_GITHUB_SECRET = os.environ["SOCIAL_AUTH_GITHUB_SECRET"]
```

- Authorize github to login
- Revoke user tokens to invalidate them

### Select Authentication backend

- Django previously had only one authentication backend to choose from, and now it has two. Django doesn’t know which one to use when creating new users
- Replace the line user = form.save() in registration view

```python
from django.shortcuts import redirect, render, Http404


def register(request):
    if request.method == "GET":
        return render(request, "register.html", {"form": NewUserCreationForm})
    elif request.method == "POST":
        form = NewUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.backend = "django.contrib.auth.backends.ModelBackend"
            user.save()
            login(request, user)
            return redirect(reverse("dashboard"))
        else:
            return Http404("Invalid Form")
```

- This will set the backend to use when using the app's registration process
- Return a `HTTP  404` error if form is invalid

## Gmail SMTP

- Create an app password for the account
- Set the following settings

```env
EMAIL_HOST = smtp.gmail.com

EMAIL_HOST_USER = your_email@gmail.com

EMAIL_HOST_PASSWORD = generated_app_password

EMAIL_PORT = 587

EMAIL_USE_TLS = True

EMAIL_BACKEND = django.core.mail.backends.smtp.EmailBackend

DEFAULT_FROM_EMAIL = your_email@gmail.com
```

## Finalise

- Add env vars to `tox.ini` and `.travis.yml`.
- Enable password validation settings.
- Close DB and clusters if not in further use.
- Check and remove any secrets added to repository.

## Notes template

```python
```

```html

```
