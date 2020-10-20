# Django-Portfolio

Notes and code about Django-Portfolio

## Sections

- [Django-Portfolio](#django-portfolio)
  - [Sections](#sections)
  - [Structure](#structure)
  - [About the project](#about-the-project)
  - [Getting started](#getting-started)
    - [Create the project](#create-the-project)
  - [Create a Django app](#create-a-django-app)
    - [Create the files](#create-the-files)
    - [Install the app](#install-the-app)
    - [Create a View](#create-a-view)
    - [Create a HTML template](#create-a-html-template)
    - [Register URLs](#register-urls)
  - [Add a base template](#add-a-base-template)
  - [Add styling to app](#add-styling-to-app)
  - [To delete an app](#to-delete-an-app)
    - [Delete the directory](#delete-the-directory)
    - [Remove it's name from installed apps](#remove-its-name-from-installed-apps)
    - [Remove url paths to it](#remove-url-paths-to-it)
  - [Create another Django app called projects](#create-another-django-app-called-projects)
  - [Projects App: Models](#projects-app-models)
  - [Create one model in models.py](#create-one-model-in-modelspy)
    - [Migrate](#migrate)
      - [Create the migrations file](#create-the-migrations-file)
      - [Migrate the app](#migrate-the-app)
    - [Create instances of class using Django shell](#create-instances-of-class-using-django-shell)
  - [Projects App: Views](#projects-app-views)
    - [Index View](#index-view)
    - [Project Detail View](#project-detail-view)
  - [Attach views to URLs](#attach-views-to-urls)
    - [Attach the app urls](#attach-the-app-urls)
    - [Hook these URLs up to the project URLs. In `personal_portfolio/urls.py`](#hook-these-urls-up-to-the-project-urls-in-personal_portfoliourlspy)
  - [Projects App: Templates](#projects-app-templates)
    - [The project_index template](#the-project_index-template)
    - [The project_detail.html template](#the-project_detailhtml-template)
  - [Create a blog](#create-a-blog)
    - [Create a new app](#create-a-new-app)
    - [Install the blog app](#install-the-blog-app)
    - [Create the blog app model](#create-the-blog-app-model)
      - [Categorty](#categorty)
      - [Post](#post)
      - [Comments](#comments)
    - [Migrate the blog models](#migrate-the-blog-models)
  - [Use the Django Admin](#use-the-django-admin)
  - [Add the views](#add-the-views)
  - [Show blog posts](#show-blog-posts)
    - [The life cycle of submitting a form](#the-life-cycle-of-submitting-a-form)
    - [Create urls.py file inside blog/](#create-urlspy-file-inside-blog)
    - [Add blog/ to project urls](#add-blog-to-project-urls)
  - [Add the blog templates](#add-the-blog-templates)
    - [Create the blog index in a new file blog/templates/blog_index.html](#create-the-blog-index-in-a-new-file-blogtemplatesblog_indexhtml)
    - [Create file blog/templates/blog_category.html for the blog_category template](#create-file-blogtemplatesblog_categoryhtml-for-the-blog_category-template)
    - [Create the blog_detail template at blog/templates/blog_detail.html](#create-the-blog_detail-template-at-blogtemplatesblog_detailhtml)
    - [Add a link to the blog_index to the navigation bar in base.html](#add-a-link-to-the-blog_index-to-the-navigation-bar-in-basehtml)
  - [Additional Information](#additional-information)
    - [Screenshots](#screenshots)
    - [Links](#links)
  - [Notes template](#notes-template)

## Structure

- A Django website consists of a single project that is split into separate apps.
- The idea is that each app handles a self-contained function that the site needs to perform.
- As an example, imagine an application like Instagram
  - User management: Login, logout, register, and so on
  - The image feed: Uploading, editing, and displaying images
  - Private messaging: Private messages between users and notifications
- These are each separate pieces of functionality, so if this were a Django site, then each piece of functionality should be a different Django app inside a single Django project.
- The Django project holds some configurations that apply to the project as a whole, such as project settings, URLs, shared templates and static files.
- Each application can have its own database and has its own functions to control how the data is displayed to the user in HTML templates. The apps simply manipulate the templates, thus providing functionality.
- Each application also has its own URLs as well as its own HTML templates and static files, such as JavaScript and CSS.
- Django apps are structured so that there is a separation of logic. It supports the **Model-View-Controller** Pattern, which is the architecture on which most web frameworks are built.
- The basic principle is that in each application there are three separate files that handle the three main pieces of logic separately
  - Model defines the data structure. This is usually a database and is the base layer to an application.
  - View displays some or all of the data to the user with HTML and CSS.
  - Controller handles how the database and the view interact.
- In Django, the architecture is slightly different. Although based upon the MVC pattern, Django handles the controller part itself. There’s no need to define how the database and views interact.
- The pattern Django utilizes is called the Model-View-Template (MVT) pattern. The view and template in the MVT pattern make up the view in the MVC pattern. All you need to do is add some URL configurations to map the views to, and Django handles the rest.
- The URL configurations each return a resource or an action, which utilise the templates and views.

## About the project

- **A fully functioning blog**: In this application, you will be able to create, update, and delete blog posts. Posts will have categories that can be used to sort them.
- **A portfolio of your work**: Showcase previous web development projects here. Build a gallery style page with clickable links to projects that are completed.

## Getting started

- Install django into a virtual environment

### Create the project

- CD into `portfolio` folder
- Create a new project with `django-admin startproject personal_portfolio`
- This will create a new directory `personal_portfolio`. If you `cd` into this new directory you’ll see another directory called `personal_portfolio` and a file called `manage.py`.
- Your directory structure should look something like this

```txt
rp-portfolio/
│
├── personal_portfolio/
│   ├── personal_portfolio/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   │
│   └── manage.py
│
└── venv/
```

- Reorder this slightly by moving all the files up a directory
- You should end up with something like this

```txt
rp-portfolio/
│
├── personal_portfolio/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── venv/
│
└── manage.py
```

- Once your file structure is set up, you can now start the server and check that your set up was successful.
- In the console, run the command `python manage.py runserver`
- Then, in your browser go to `localhost:8000`, and you should see the django welcome page.

## Create a Django app

- Create a hello world app to get started.

### Create the files

- In the console, run the command `python manage.py startapp hello_world`
- This will create another directory called hello_world with several files
  - `__init__`.py tells Python to treat the directory as a Python package.
  - `admin.py` contains settings for the Django admin pages.
  - `apps.py` contains settings for the application configuration.
  - `models.py` contains a series of classes that Django’s ORM converts to database tables.
  - `tests.py` contains test classes.
  - `views.py` contains functions and classes that handle what data is displayed in the HTML templates.

### Install the app

- In `rp-portfolio/settings.py`, add the following line of code under `INSTALLED_APPS`

```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "hello_world",  # Add this line
]
```

- The project now knows that the app you just created exists. Now, we create a view to display something to a user.

### Create a View

- Views in Django are a collection of functions or classes inside the views.py file in your app directory.
- Each function or class handles the logic that gets processed each time a different URL is visited.
- A view is what handles the request send to the server. It returns a template as a render object, or handles some other functionality.
- Navigate to the `views.py` file in the `hello_world` directory.
- There’s already a line of code in there that imports `render()`.
- Add the following code

```python
from django.shortcuts import render

# Add these lines
def hello_world(request):
    return render(request, "hello_world.html", {})
```

- This defined a view function called `hello_world()`.
- When this function is called, it will render an HTML file called `hello_world.html`.
- The view function takes one argument, `request`.
- This object is an `HttpRequestObject` that is created whenever a page is loaded.
- It contains information about the `request`, such as the method, which can take several values including `GET` and `POST`.

### Create a HTML template

- We now need to create the HTML template to display to the user.
- `render()` looks for HTML templates inside a directory called `templates` inside the app's directory(App being `hello_world` here).
- This function will handle views and templates to display to the user.
- Create that directory and subsequently a file named `hello_world.html` inside it

```cmd
mkdir hello_world/templates/
echo. >> hello_world/templates/hello_world.html
```

- Add `<h1>Hello, World!</h1>` to the `hello_world.html` file

### Register URLs

- The final step is to hook up URLs so that users can visit the page.
- The project has a module called `urls.py` in which we need to include a URL configuration for the `hello_world` app.
- Inside `personal_portfolio/urls.py`, add

```python
from django.contrib import admin
from django.urls import path, include  # Add this line

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("hello_world.urls")),  # Add this line
]
```

- This looks for a module called `urls.py` inside the `hello_world` application and **registers any URLs defined there**.
- Whenever there is a visitto  the root path of the server's URL (localhost:8000), the `hello_world` application’s URLs will be registered.
- Create the `hello_world.urls` module as `hello_world/urls.py`
- Inside this module, we need to import the `path` object as well as our app’s `views` module.
- Then we want to create a list of URL patterns that correspond to the various view functions.
- At the moment, we have only created one view function, so we need only create one URL.

```python
from django.urls import path
from hello_world import views

urlpatterns = [path("", views.hello_world, name="hello_world")]
```

- Restart the server and visit localhost:8000 to see the HTML template just created.
- We have created our first Django app and hooked it up to our project.

## Add a base template

Create a base template to add to each app of the project.

- In the console, run the command `mkdir personal_portfolio/templates/`
- Create the file `personal_portfolio/templates/base.html`

Create this additional `templates` directory to store HTML templates that will be used in every Django app in the project. Each Django project can consist of multiple apps that handle separated logic, and each app contains its own templates directory to store HTML templates related to the application.

This application structure works well for the back end logic, but we want our entire site to look consistent on the front end. Instead of having to import Bootstrap styles into every app, we can create a template or set of templates that are shared by all the apps. As long as Django knows to look for templates in this new, shared directory it can save a lot of repeated styles.

Whenever we want to create templates or import scripts that are intended to be used in all Django apps inside a project, we can add them to this project-level directory and extend them inside our app templates.

- Inside `personal_portfolio/templates/base.html` add the following

```html
{% block page_content %}{% endblock %}
```

- Inside `hello_world/templates/hello_world.html` add the following

```html
{% extends "base.html" %}

{% block page_content %}
<h1>Hello, World!</h1>
{% endblock %}
```

What happens here is that any HTML inside the page_content block gets added inside the same block in `base.html`.

This will then show up in every page that extends `base.html`.

We now need to tell our our Django project that `base.html` exists. The default settings register template directories in each app, but not in the project directory itself.

In `personal_portfolio/settings.py`, update `TEMPLATES` list

```python
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            "personal_portfolio/templates/"
        ],  # register template directories inthe project directory itself
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

## Add styling to app

Add `Bootstrap`, or any classless CSS to the entire project.

Add the stylesheet inside `base.html`'s `page_content` block.

Visiting `localhost:8000`, should show that the page has been formatted with slightly different styling.

## To delete an app

- Delete the `hello_world` application

### Delete the directory

- Delete the `hello_world` directory

### Remove it's name from installed apps

- Remove the line `"hello_world"`, from `INSTALLED_APPS` in `settings.py`

```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "hello_world",  # Delete this line
]
```

### Remove url paths to it

- Remove the URL path created in `personal_portfolio/urls.py`

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("hello_world.urls")),  # Delete this line
]
```

## Create another Django app called projects

- In the console, run the command `python manage.py startapp projects`
- Add to list of installed apps

```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "projects",
]
```

## Projects App: Models

Django has a built-in **Object Relational Mapper (ORM)**.

An **ORM is a program that allows you to create classes that correspond to database tables**. Class attributes correspond to columns, and instances of the classes correspond to rows in the database. So, instead of learning a whole new language to create our database and its tables, we can just write some Python classes.

## Create one model in models.py

The model you’ll create will be called `Project` and will have the following fields:

- **title** will be a short string field to hold the name of your project.
- **description** will be a larger string field to hold a longer piece of text.
- **technology** will be a string field, but its contents will be limited to a select number of choices.
- **image** will be an image field that holds the file path where the image is stored.

To create this model, we’ll create a new class in `models.py` and add the following in our fields

```python
from django.db import models


class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    technology = models.CharField(max_length=20)
    image = models.FilePathField(path="/img")
```

Django models come with many built-in model field types. We’ve only used three in this model. `CharField` is used for short strings and specifies a maximum length.

`TextField` is similar to `CharField` but can be used for longer form text as it doesn’t have a maximum length limit. Finally, `FilePathField` also holds a string but must point to a file path name.

Now that we’ve created our `Project` class, we need Django to create the database. By default, the Django ORM creates databases in SQLite, but you can use other databases that use the SQL language, such as PostgreSQL or MySQL, with the Django ORM.

### Migrate

To start the process of creating our database, we need to create a migration. A migration is a file containing a Migration class with rules that tell Django what changes need to be made to the database.

#### Create the migrations file

To create the migration, type the `makemigrations` command in the console, making sure you’re in the `rp-portfolio` directory

```bash
$ python manage.py makemigrations projects
Migrations for 'projects':
  projects/migrations/0001_initial.py
    - Create model Project
```

You should see that a file `projects/migrations/0001_initial.py` has been created in the `projects` app. Check out that file in the [source code](https://github.com/realpython/materials/blob/0091ee5421f8107e8629f1f22687ff224850b889/rp-portfolio/projects/migrations/0001_initial.py) to make sure your migration is correct.

#### Migrate the app

Now that you’ve create a migration file, you need to apply the migrations set out in the migrations file and create your database using the `migrate` command:

```bash
$ python manage.py migrate projects
Operations to perform:
  Apply all migrations: projects
Running migrations:
  Applying projects.0001_initial... OK
```

You should also see that a file called `db.sqlite3` has been created in the root of your project.

When running both the `makemigrations` and `migrate` commands, we added `projects` to our command. This tells Django to only look at models and migrations in the `projects` app. Django comes with several models already created.

If you run `makemigrations` and `migrate` without the projects flag, then all migrations for all the default models in your Django projects will be created and applied.

### Create instances of class using Django shell

To create instances of our `Project` class, we’re going to have to use the **Django shell**. The Django shell is similar to the Python shell but allows you to access the database and create entries. To access the Django shell, we use `python manage.py shell`.

Once you’ve accessed the shell, you’ll notice that the command prompt will change from `$ to >>>`. You can then import your models.

```python
from projects.models import Project
```

We’re first going to create a new project with the following attributes:

**name**: My First Project
**description**: A web development project.
**technology**: Django
**image**: img/project1.png

To do this, we create an instance of the Project class in the Django shell

```python
p1 = Project(
    title="My First Project",
    description="A web development project.",
    technology="Django",
    image="img/project1.png",
)
p1.save()
```

This creates a new entry in your projects table and saves it to the database. Now you have created a project that you can display on your portfolio site.

The create two more sample projects

```python
p2 = Project(
    title="My Second Project",
    description="Another web development project.",
    technology="Flask",
    image="img/project2.png",
)
p2.save()
p3 = Project(
    title="My Third Project",
    description="A final development project.",
    technology="Django",
    image="img/project3.png",
)
p3.save()
```

## Projects App: Views

We will now create view functions to send the data from the database to the HTML templates.

In the projects app,

An index view that shows a snippet of information about each project
A detail view that shows more information on a particular topic

### Index View

- Import the `Project` class from `models.py`
- Create a function `project_index()` that renders a template called `project_index.html`
  - In the body of this function, create a Django ORM query to select all objects in the Project table

```python
from django.shortcuts import render
from projects.models import Project


def project_index(request):
    projects = Project.objects.all()
    context = {"projects": projects}
    return render(request, "project_index.html", context)
```

Here, it performs a query. A query is simply a command that allows you to create, retrieve, update, or delete objects (or rows) in your database. A database query returns a collection of all objects that match the query, known as a Queryset. In this case, you want all objects in the table, so it will return a collection of all projects.

We define a dictionary `context`. The dictionary only has one entry projects to which we assign our `Queryset` containing all projects. The `context` dictionary is used to send information to our template. **Every view function you create needs to have a context dictionary.**

Context is added as an argument to `render()`. Any entries in the context dictionary are available in the template, as long as the context argument is passed to `render()`. We also render a template named `project_index.html`.

### Project Detail View

- The `project_detail()` view function.
- This function will need an additional argument: the id of the project that’s being viewed.

```python
def project_detail(request, pk):
    project = Project.objects.get(pk=pk)
    context = {"project": project}
    return render(request, "project_detail.html", context)
```

We perform a query. This query retrieves the project with primary key, `pk`, equal to that in the function argument. We then assign that project in our `context` dictionary, which we pass to `render()`. Again, there’s a template `project_detail.html`.

## Attach views to URLs

### Attach the app urls

Create a file `projects/urls.py` to hold the URL configuration for the app.

```python
from django.urls import path
from . import views

urlpatterns = [
    path("", views.project_index, name="project_index"),
    path("<int:pk>/", views.project_detail, name="project_detail"),
]
```

- Hook up the root URL of our app to the `project_index` view.
- To hook up the `project_detail` view, we want the URL to be /1, or /2, and so on, depending on the pk of the project. To do this, we used the `<int:pk>` notation. This just tells Django that the value passed in the URL is an integer, and its variable name is pk.

### Hook these URLs up to the project URLs. In `personal_portfolio/urls.py`

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("projects/", include("projects.urls")),
]
```

This line of code includes all the URLs in the projects app but means they are accessed when prefixed by `projects/`. There are now two full URLs that can be accessed with our project

- localhost:8000/projects: The project index page
- localhost:8000/projects/3: The detail view for the project with pk=3

## Projects App: Templates

Create the HTML templates for the views.

1. The project_index template
2. The project_detail template

### The project_index template

Create a grid of cards, with each card displaying details of the project, each dynamically generated.

- Add Bootstrap styles to our application in `base.html`
- The for loop syntax in the Django template engine is as follows:

```html
{% for project in projects %}
{# Do something... #}
{% endfor %}
```

- Create `projects/templates/project_index.html`

```html
{% extends "base.html" %} {% load static %} {% block page_content %}
{{block.super }}

<body>
  <main>
    <section>
      <h1>Projects</h1>
    </section>
    <section class="row">
      {% for project in projects %}
      <section class="col-md-4">
        <div class="card mb-2">
          <img
            class="card-img-top"
            src="{% static project.image %}"
            alt="Project Image"
          />
          <div class="card-body">
            <h5 class="card-title">{{project.title}}</h5>
            <p class="card-text">{{project.description}}</p>
            <a
              href="{% url 'project_details' project.id %}"
              class="btn btn-primary"
              >Read more</a
            >
          </div>
        </div>
      </section>
      {% endfor %}
    </section>
  </main>
</body>

{% endblock %}

```

- We extend `base.html`
- We include a `{% load static %}` tag to include static files such as images
- When loading static files, Django looks in the static/ directory for files matching a given filepath within static/.
- Create a directory named `static/` with another 2 directories named `projects/img/` inside.
- Copy over the images from [here](https://github.com/realpython/materials/tree/7909f5a682a88d8488167bc6fe9b64a5b294f99a/rp-portfolio/projects/static/img).
- we begin the `for` loop, looping over all `projects` passed in by the `context` dictionary. Inside this for loop, we can access each individual project. To access the project’s attributes, use dot notation inside double curly brackets. For example, to access the project’s title, use `{{ project.title }}`. The same notation can be used to access any of the project’s attributes.
- Include project image. Inside the `src` attribute, we add the code `{% static project.image %}.` This tells Django to look inside the static files to find a file matching `project.image`.
- Link to `project_detail` page. Accessing URLs in Django is similar to accessing static files. The code for the URL has the following form: `{% url '<url path name>' <view_function_arguments> %}`
- We are accessing a URL path named `project_detail`, which takes integer arguments corresponding to the `pk` number of the project.

### The project_detail.html template

```html
{% extends "base.html" %} {% load static %} {% block page_content %}
{{block.super }}

<body>
  <main>
    <section>
      <h1>{{project.titile}}</h1>
    </section>
    <section class="row">
      <div class="col-md-8">
        <img
          src="{% static project.image %}"
          alt="Project Image"
          width="100%"
        />
      </div>
      <div class="col-md 4">
        <h5>About the project</h5>
        <p>{{project.description}}</p>
        <br />
        <h5>Technology used</h5>
        <p>{{project.technology}}</p>
      </div>
    </section>
  </main>
</body>
{% endblock %}

```

- The template exists for each project in the Project model.
- To access the project’s image, use `{{ project.image }}`.
- To access the project’s title, use `{{ project.title }}`.
- To access the project’s description, use `{{ project.description }}`.
- To access the project’s technology, use `{{ project.technology }}`.

## Create a blog

### Create a new app

- In the console, run the command `python manage.py startapp blog`

### Install the blog app

```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "projects",
    "blog",
]
```

### Create the blog app model

We create 3 models: Category, Post, Comment

#### Categorty

```python
from django.db import models

# Category model


class Category(models.Model):
    """
    Model for categories. Each instance is a category.
    """

    name = models.CharField(max_length=20)
```

- `name` is a `CharField` we store the name of the category.

#### Post

```python
class Post(models.Model):
    """
    Model for all posts. Each instance is a post with title, body, and dates
    of creation and modification. Also has a many to many relation to
    Categories.
    """

    title = models.CharField(max_length=255)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField("Category", related_name="posts")
```

- `created_on` and `last_modified`, are Django `DateTimeFields`.
- These store a datetime object containing the date and time when the post was created and modified respectively.
- When `DateTimeField` takes an argument `auto_now_add=True`. This assigns the current date and time to this field whenever an instance of this class is created.
- When `DateTimeField` takes an argument `auto_now=True`. This assigns the current date and time to this field whenever an instance of this class is saved. That means whenever you edit an instance of this class, the date_modified is updated.
- We want to link our models for categories and posts in such a way that many categories can be assigned to many posts. We use `ManytoManyField` field type.
- This field links the `Post` and `Category` models and allows us to create a relationship between the two tables.
- The `ManyToManyField` takes two arguments. The first is the model with which the relationship is, in this case its `Category`. The second allows us to access the relationship from a `Category` object, even though we haven’t added a field there. By adding a `related_name` of posts, we can access `category.posts` to give us a list of posts with that `category`.

#### Comments

```python
class Comments(models.Model):
    """
    Model for all comments. Each instance is a comment with author, body,
    created_on, and the post it is related to is a ForeignKey.
    """

    author = models.CharField(max_length=60)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
```

- There’s an `author` field for users to add a name or alias, a `body` field for the body of the comment, and a `created_on` field that is identical to the `created_on` field on the `Post` model.
- the `ForeignKey` field is similar to the `ManyToManyField` but instead defines a **many to one** relationship. The reasoning behind this is that many comments can be assigned to one post. But you can’t have a comment that corresponds to many posts.
- The `ForeignKey` field takes two arguments. The first is the other model in the relationship, in this case, `Post`. The second tells Django what to do when a post is deleted. If a post is deleted, then we don’t want the comments related to it hanging around. We, therefore, want to delete them as well, so we add the argument `on_delete=models.CASCADE`

### Migrate the blog models

- Create the migration files with makemigrations: `python manage.py makemigrations blog`
- Migrate the tables. This time, don’t add the app-specific flag, so that this can be used later: `python manage.py migrate`

## Use the Django Admin

It allows you to create, update, and delete instances of your model classes and provides a nice interface for doing so. Before you can access the admin, you need to add yourself as a superuser. This is why, in the previous section, you applied migrations project-wide as opposed to just for the app. Django comes with built-in user models and a user management system that will allow you to login to the admin.

- Add yourself as superuser using the following command: `python manage.py createsuperuser`
- Enter a username followed by an email address and a password.
- Navigate to `localhost:8000/admin` and log in with the credentials.
- The `User` and `Groups` models should appear, but you’ll notice that there’s no reference to the models you’ve created yourself. That’s because you need to register them inside the admin.
- Open the file `blog/admin.py`
- Import the models you want to register on the admin page.
  - Define empty classes `PostAdmin` and `CategoryAdmin`.
  - Adding attributes can customize what is shown on the admin page.

```python
from blog.models import Category, Comments, Post
from django.contrib import admin


# Register your models here.
class PostAdmin(admin.ModelAdmin):
    pass


class CommentAdmin(admin.ModelAdmin):
    pass


class CategoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comments, CommentAdmin)
```

- If you wanted to add a feature where comments are moderated, then go ahead and add the `Comments` model too.
- Visit `localhost:8000/admin`, and see that the `Comments`, `Post` and `Category` models are now visible. Add new instances of both models.

## Add the views

Create three view functions in the views.py file in the blog directory:

- **blog_index** will display a list of all your posts.
- **blog_detail** will display the full post as well as comments and a form to allow users to create new comments.
- **blog_category** will be similar to blog_index, but the posts viewed will only be of a specific category chosen by the user.

- In `blog/views.py`

```python
import logging

from blog.forms import CommentForm
from blog.models import Comments, Post
from django.shortcuts import render

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def blog_index(request):
    posts = Post.objects.all().order_by("-created_on")
    context = {"posts": posts}
    return render(request, "blog_index.html", context)
```

- All posts are queried and odrdered by `-created_on`, which means most recent post. `-` tells Django to start with the largest value rather than the smallest.

- Create the `blog_category()` view

```python
def blog_category(request, category):
    posts = Post.objects.filter(categories__name__contains=category).order_by(
        "-created_on"
    )
    context = {"category": category, "posts": posts}

    return render(request, "blog_category.html", context)
```

- Uses [Django Queryset filter](https://docs.djangoproject.com/en/2.1/topics/db/queries/#retrieving-specific-objects-with-filters).
- The argument of the filter tells Django what conditions need to be met for an object to be retrieved. In this case, we only want posts whose categories contain the category with the name corresponding to that given in the argument of the view function.

## Show blog posts

- We are going to include a comment form so that people can comment on the post.
- To add a form to the page, create another file in the blog directory named `forms.py`.
- Django forms are very similar to models.
- A form consists of a class where the class attributes are form fields.
- Django comes with some built-in form fields.
- For this form, the only fields are `author`, which should be a `CharField`, and `body`, which can also be a `CharField`.
- If the `CharField` of your form corresponds to a model `CharField`, make sure both have the same `max_length` value.

- In `blog/forms.py`

```python
from django import forms


class CommentForm(forms.Form):
    author = forms.CharField(
        max_length=60,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Name"}),
    )
    body = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "placeholder": "Comment"})
    )
```

- `Widget` has been passed to both the fields. The author field has the `forms.TextInput` widget. This tells Django to load this field as an HTML text input element in the templates. The body field uses a `forms.TextArea` widget instead, so that the field is rendered as an HTML text area element.
- These widgets also take an argument `attrs`, which is a dictionary and allows us to specify some CSS classes, which will help with formatting the template for this view later. It also allows us to add some placeholder text.

- Create the `blog_detail()` view

```python
def blog_detail(request, pk):
    post = Post.objects.get(pk=pk)
    comments = Comment.objects.filter(post=post)
    context = {"post": post, "comments": comments}

    return render(request, "blog_detail.html", context)
```

- Set up the view function to show a specific post with a comment associated with it.
- The view function takes a `pk` value as an argument and retrieves the object with the given `pk`.
- We retrieve all the comments assigned to the given post using Django filters again.
- Lastly, add both post and comments to the context dictionary and render the template.

- When a form is posted, a POST request is sent to the server.
- Check if a POST request has been received and then create a comment from the form fields.
- Django comes with a handy `is_valid()` on its forms, so we can check that all the fields have been entered correctly.
- Create the comment from the form, save it using `save()` and then query the database for all the comments assigned to the given post.

```python
def blog_detail(request, pk):
    post = Post.objects.get(pk=pk)
    logger.debug("start")

    form = CommentForm()

    if request.method == "POST":
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = Comments(
                author=form.cleaned_data["author"],
                body=form.cleaned_data["body"],
                post=post,
            )
            comment.save()
        else:
            logger.error("Invalid form")

    comments = Comments.objects.filter(post=post)
    context = {"post": post, "comments": comments, "form": form}

    return render(request, "blog_detail.html", context)
```

- If a `POST` request has been received then we create a new instance of our form, populated with the data entered into the form.
- The form is then validated using `is_valid()`. If the form is valid, a new instance of `Comment` is created.
- You can access the data from the form using `form.cleaned_data`, which is a dictionary.
- They keys of the dictionary correspond to the form fields, so you can access the author using form.cleaned_data['author'].
- Add the current post to the comment when you create it.

### The life cycle of submitting a form

- When a user visits a page containing a form, they send a GET request to the server. In this case, there’s no data entered in the form, so we just want to render the form and display it.
- When a user enters information and clicks the Submit button, a POST request, containing the data submitted with the form, is sent to the server. At this point, the data must be processed, and two things can happen:
  1. The form is valid, and the user is redirected to the next page.
  2. The form is invalid, and empty form is once again displayed. The user is back at step 1, and the process repeats.

The Django forms module will output some errors, [which you can display to the user.](https://docs.djangoproject.com/en/2.1/topics/forms/#rendering-form-error-messages).

### Create urls.py file inside blog/

```python
from django.urls import path
from . import views

urlpatterns = [
    path("", views.blog_index, name="blog_index"),
    path("<int:pk>/", views.blog_detail, name="blog_detail"),
    path("<category>/", views.blog_category, name="blog_category"),
]
```

### Add blog/ to project urls

Once the blog-specific URLs are in place, add them to the projects URL configuration using `include()`

```python
"""personal_portfolio URL Configuration

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
    path("projects/", include("projects.urls")),
    path("blog/", include("blog.urls")),
]
```

All the blog URLs will be prefixed with blog/, and you’ll have the following URL paths:

- localhost:8000/blog: Blog *index*
- localhost:8000/blog/1: Blog detail view of blog with *pk=1*
- localhost:8000/blog/python: Blog index view of all posts with category *python*

They each correspond to a view function in `blog/`

## Add the blog templates

### Create the blog index in a new file blog/templates/blog_index.html

- Extend the base template `personal_porfolio/templates/base.html`
- Use a for loop to loop over all the posts.
- For each post, display the title and a snippet of the body.

```html
{% extends "base.html" %} {% load static %} {% block page_content %}
{{block.super }}

<body>
  <main>
    <section class="col-md-8 offset-md-2">
      <h1>Blog Index</h1>
      <hr />
      {% for post in posts %}
      <h2><a href="{% url 'blog_detail' post.pk %}">{{post.title}}</a></h2>
      <small>
        {{post.created_on.date}} |&nbsp; Categories:&nbsp; {% for category in
        post.categories.all %}
        <a href="{% url 'blog_category' category.name %}"> {{category.name}} </a
        >&nbsp; {% endfor %}
      </small>
      <p>{{post.body | slice:":400"}}...</p>
      {% endfor %}
    </section>
  </main>
</body>

{% endblock %}

```

- `<h2><a href="{% url 'blog_detail' post.pk%}">{{ post.title }}</a></h2>` has the post title
- The link is a Django link where we are pointing to the URL named blog_detail, which takes an integer as its argument and should correspond to the pk value of the post.
- We use another for loop to loop over all the categories assigned to the post.
- We use a template filter `slice` to cut off the post body at 400 characters so that the blog index is more readable.
- Access this page by visiting `localhost:8000/blog`

### Create file blog/templates/blog_category.html for the blog_category template

Identical to blog_index.html, except with the category name inside the `h1` tag instead of Blog Index

```html
{% extends "base.html" %} {% load static %} {% block page_content %}
{{block.super }}

<body>
  <main>
    <section class="col-md-8 offset-md-2">
      <h1>{{ category | title}}</h1>
      <hr />
      {% for post in posts %}
      <h2><a href="{% url 'blog_detail' post.pk %}">{{post.title}}</a></h2>
      <small>
        {{post.created_on.date}} |&nbsp; Categories:&nbsp; {% for category in
        post.categories.all %}
        <a href="{% url 'blog_category' category.name %}"> {{category.name}} </a
        >&nbsp; {% endfor %}
      </small>
      <p>{{post.body | slice:":400"}}</p>
      {% endfor %}
    </section>
  </main>
</body>

{% endblock %}

```

- We use the Django template filter `title`. This applies **titlecase** to the string and makes words start with an uppercase character.

- Visit `localhost:8000/blog/python` and see all the posts with that category.

### Create the blog_detail template at blog/templates/blog_detail.html

- Display the date the post was created and any categories.
- Underneath that include a comments form so users can add a new comment.
- Under this, there will be a list of comments that have already been left.

```html
{% extends "base.html" %} {% load static %} {% block page_content %}
{{block.super }}

<body>
  <main>
    <section class="col-md8 offset-md-2">
      <h1>{{post.title}}</h1>
      <small
        >{{post.created_on.date}} |&nbsp; Categories:&nbsp; {% for category in
        post.categories.all %}
        <a href="{% url 'blog_category' category.name %}">{{category.name}}</a
        >&nbsp; {% endfor %}
      </small>
      <p>{{post.body | linebreaks}}</p>
      <h3>Leave a comment:</h3>
      <form action="/blog/{{post.pk}}/" method="POST">
        {% csrf_token %}
        <div class="form-group">{{form.author}}</div>
        <div class="form-group">{{form.body}}</div>
        <button type="submit" class="btn btn-primary">Submit</button>
      </form>
      <h3>Comments:</h3>
      {% for comment in comments %}
      <p>
        On {{comment.created_on.date}}&nbsp;
        <b>{{comment.author}}</b> &nbsp;wrote:
      </p>
      <p>{{comment.body}}</p>
      <hr />
      {% endfor %}
    </section>
  </main>
</body>

{% endblock %}

```

- Loop over all the categories of the post.
- When rendering the post body, use a `linebreaks` template filter. This tag registers line breaks as new paragraphs, so the body doesn’t appear as one long block of text.
- Underneath the post display the comment form.
- The form action points to the URL path of the page to which you’re sending the POST request to.
- In this case, it’s the same as the page that is currently being visited.
- Add a `csrf_token`, which provides security and renders the body and author fields of the form, followed by a submit button.
- To get the bootstrap styling on the author and body fields, you need to add the form-control class to the text inputs.
- Because Django renders the inputs for you when you include {{ form.body }} and {{ form.author }}, you can’t add these classes in the template. That’s why you added the attributes to the form widgets in the previous section.
- Underneath the form, there’s another for loop that loops over all the comments on the given post. The comments, body, author, and created_on attributes are all displayed.
- Visit `localhost:8000/blog/1` and view your first post.

### Add a link to the blog_index to the navigation bar in base.html

```html
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">

<nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container">
        <a class="navbar-brand" href="{% url 'project_index' %}">RP Portfolio</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav mr-auto">
            <li class="nav-item active">
              <a class="nav-link" href="{% url 'project_index' %}">Home</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="{% url 'blog_index' %}">Blog</a>
            </li>
          </ul>
        </div>
    </div>

</nav>

<div class="container">
    {% block page_content %}{% endblock %}
</div>

<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" integrity="sha384-ZMP7rVo3mIykV+2+9J [≈ flash energy of a typical pocket camera photoflash capacitor, 100-400 µF @ 330 V]3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49" crossorigin="anonymous"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js" integrity="sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy" crossorigin="anonymous"></script>

```

## Additional Information

### Screenshots

### Links

## Notes template

```python
```

In the console, run the command ``
