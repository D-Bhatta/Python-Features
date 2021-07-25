# OpenCV-Masker-Django

Notes and code about OpenCV-Masker-Django

## Sections

- [OpenCV-Masker-Django](#opencv-masker-django)
  - [Sections](#sections)
  - [Notes](#notes)
  - [Create project and deploy](#create-project-and-deploy)
    - [Main tasks](#main-tasks)
    - [Create a django project `django_apps`](#create-a-django-project-django_apps)
    - [Create a django app called `opencv_masker`](#create-a-django-app-called-opencv_masker)
    - [Deploy to pythonanywhere](#deploy-to-pythonanywhere)
  - [A homepage where people upload their videos through an upload form](#a-homepage-where-people-upload-their-videos-through-an-upload-form)
    - [Main tasks](#main-tasks-1)
    - [Create a view](#create-a-view)
    - [Create a homepage](#create-a-homepage)
    - [Add a form element with a dummy link](#add-a-form-element-with-a-dummy-link)
    - [Add the videos](#add-the-videos)
    - [Link the form](#link-the-form)
    - [Research how to upload files and use checklists](#research-how-to-upload-files-and-use-checklists)
  - [Modify form to upload files](#modify-form-to-upload-files)
  - [Create an API that will take the input video, and return an output video url](#create-an-api-that-will-take-the-input-video-and-return-an-output-video-url)
    - [Main tasks](#main-tasks-2)
    - [Create a view that takes a form request](#create-a-view-that-takes-a-form-request)
    - [Get video from the request and store it if necessary](#get-video-from-the-request-and-store-it-if-necessary)
    - [Get output url](#get-output-url)
    - [Refactor homepage](#refactor-homepage)
  - [Create a class that will mask colors in a video](#create-a-class-that-will-mask-colors-in-a-video)
    - [Main Tasks](#main-tasks-3)
    - [Create a class `Masker`](#create-a-class-masker)
    - [Add an input function that gets the video](#add-an-input-function-that-gets-the-video)
    - [Add an output function that returns a video url](#add-an-output-function-that-returns-a-video-url)
    - [Add mask related functions](#add-mask-related-functions)
    - [Add video writing functions](#add-video-writing-functions)
    - [Add more colors](#add-more-colors)
    - [Refactor the class](#refactor-the-class)
  - [Create a view that returns the video in a page](#create-a-view-that-returns-the-video-in-a-page)
    - [Main tasks](#main-tasks-4)
    - [Create a view and url to display the video with context](#create-a-view-and-url-to-display-the-video-with-context)
  - [Create a template to display the video](#create-a-template-to-display-the-video)
    - [Show warning to download or video will disappear](#show-warning-to-download-or-video-will-disappear)
    - [Pass it to class `Masker` function `apply_mask`](#pass-it-to-class-masker-function-apply_mask)
  - [Add a form check list with `blue` and `red` on it](#add-a-form-check-list-with-blue-and-red-on-it)
  - [Refactor `views.video` to call `Masker.apply_mask` with color in form](#refactor-viewsvideo-to-call-maskerapply_mask-with-color-in-form)
  - [Additional Information](#additional-information)
    - [Screenshots](#screenshots)
    - [Links](#links)
  - [Notes template](#notes-template)

<!-- markdownlint-disable-file MD024 -->

## Notes

## Create project and deploy

- Create a django project
- Deploy to python anywhere

### Main tasks

- Create a django project `django_apps`
- Create a django app called `opencv_masker`
- Deploy to pythonanywhere

### Create a django project `django_apps`

- Create the project with `django-admin startproject django_apps`

### Create a django app called `opencv_masker`

- Create an app with `python manage.py startapp opencv_masker`
- Install app

```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "opencv_masker",
]
```

- Run and refactor
- Remove secret key in `settings.py`

```python
SECRET_KEY = ""
```

- Add key generation utility in `utils.py` in `django_apps`

```python
from django.core.management.utils import get_random_secret_key


def generate_secret_key(env_file_name):
    r"""Generates a secret key and stores inside a `.env` file

    Generates a secret key for Django's `settings.py`. Stores it in a `.env`
    file with filename `env_file_name`.
    This can later be retrieved and set as an environment variable.

    Parameters
    ----------
    env_file_name : string
        Name of the `.env` file

    Returns
    -------
    None

    References
    ----------
    Cite the relevant literature, e.g. [1]_.  You may also cite these
    references in the notes section above.

    .. [1] Distributing Django projects with unique SECRET_KEYs
    https://stackoverflow.com/a/49362490

    Examples
    --------
    in the `setting.py` file of a django project, write the following lines of
    code. This will generate and set a DJANGO_SECRET_KEY as an environment
    variable.

    import dotenv
    from [project-folder-name] import utils
    ...
    try:
        SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
    except KeyError:
        path_env = os.path.join(BASE_DIR, '.env')
        utils.generate_secret_key(path_env)
        dotenv.read_dotenv(path_env)
        SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
    """
    with open(env_file_name, "a+") as f:
        generated_key = get_random_secret_key()
        f.write(f"DJANGO_SECRET_KEY = {generated_key}\n")
```

- Use `dotenv` to set environment variables in `settings.py`

```python
import dotenv
from django_apps import utils
import os

""" ... """

# Retrieve the environment variables

CONFIG_DIR = Path(__file__).resolve().parent.parent.parent.parent
try:
    path_env = os.path.join(CONFIG_DIR, ".env")
    dotenv.read_dotenv(path_env)
except EnvironmentError:
    print("Couldn't retrieve the environment variables")

try:
    path_env = os.path.join(CONFIG_DIR, ".env")
    dotenv.read_dotenv(path_env)
    SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
except KeyError:
    path_env = os.path.join(CONFIG_DIR, ".env")
    utils.generate_secret_key(path_env)
    dotenv.read_dotenv(path_env)
    SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
```

- Add to git
- Add static files in `django_apps/static/django_apps`
- Add a view to serve `dummy.html` at `masker/`

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
    path("opencv_masker/", include("opencv_masker.urls")),
]
```

```python
from django.urls import path

from opencv_masker import views

urlpatterns = [path("home/", views.homepage, name="homepage")]
```

```python
from django.shortcuts import render

# Create your views here.


def homepage(request):
    return render(request, "dummy.html", {})
```

- Add `base.html` templates

```html
{% block header_content %} {% load static %}
<html>
  <meta charset="utf-8" />
  <meta
    name="viewport"
    content="width=device-width, initial-scale=1.0, user-scalable=yes"
  />
  <link rel="stylesheet" href="{% static 'css/ridge.css' %}" />
  <link rel="stylesheet" href="{% static 'css/ridge-dark.css' %}" />
  {% endblock header_content %}
</html>

```

```python
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["django_apps/templates/"],  # Add them here
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

- Add a `dummy.html` template

```html
{% extends "base.html" %} {% load static %} {% block header_content %}
{{block.super }}
<head>
  <title>Welcome to OpenCV Masker</title>
</head>
<body>
  <main>
    <vstack spacing="s" stretch="" align-x="center" align-y="center">
      <h1>This is a dummy test page</h1>
    </vstack>
  </main>
</body>
{% endblock header_content %}

```

- Run and refactor
- Modify settings to use 2 different values depending upon environment

```python
# Find out what environment we are running in
# Get the hostname
try:
    DJANGO_ENVIRONMENT = os.environ["DJANGO_ENVIRONMENT"]
    DJANGO_HOST_NAME = os.environ["DJANGO_HOST_NAME"]
except KeyError:
    path_env = os.path.join(BASE_DIR, ".env")
    dotenv.read_dotenv(path_env)
    DJANGO_ENVIRONMENT = os.environ["DJANGO_ENVIRONMENT"]
    DJANGO_HOST_NAME = os.environ["DJANGO_HOST_NAME"]

if DJANGO_ENVIRONMENT == "PRODUCTION":
    ALLOWED_HOSTS = [DJANGO_HOST_NAME]
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "django_apps/static/django_apps"),
        os.path.join(BASE_DIR, "opencv_masker/static/opencv_masker"),
    ]
elif DJANGO_ENVIRONMENT == "DEVELOPMENT":
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "django_apps\\static\\django_apps"),
        os.path.join(BASE_DIR, "opencv_masker\\static\\opencv_masker"),
    ]
    ALLOWED_HOSTS = []
else:
    pass

STATIC_ROOT = os.path.join(BASE_DIR, "static")
```

- Run and refactor
- Add a logo

### Deploy to pythonanywhere

- Pull from git
- Create environment
- Install dependencies
- Collect static
- Follow tutorial [here](https://help.pythonanywhere.com/pages/DeployExistingDjangoProject/)
- Working and source code directories are the ones with `manage.py` in them
- Add static assets
- Enable HTTPS
- Run and refactor

## A homepage where people upload their videos through an upload form

- Create a homepage with a heading and instructions and example videos
- Add a form with upload button and a check list with `blue` and `red` on it
- Link the form destination to it

### Main tasks

- Create a view
- Create a homepage
- Add a form element with a dummy link
- Add the videos
- Link the form
- Research how to upload files and use checklists

### Create a view

- Create a `homepage` view function
- Add an url to `home/`
- Serve `dummy.html`
- Run and refactor

### Create a homepage

- Create a `homepage.html`

```html
{% extends "base.html" %} {% load static %} {% block header_content %}
{{block.super }}
<head>
  <title>OpenCV Masker</title>
</head>
<body>
  <main>
    <vstack spacing="m">
      <vstack spacing="s" stretch="" align-x="center" align-y="center">
        <h1>Welcome to OpenCV Masker</h1>
        <p>Add instructions here</p>
      </vstack>
      <spacer></spacer>
      <vstack spacing="l">
        <vstack spacing="xs">
          <aside class="pa-s">
            <vstack>
              <form action="#" method="POST">
                <!-- {% csrf_token %} -->
                <vstack spacing="s">
                  <vstack>
                    <!-- {{form}} -->
                    <input type="file" name="video" id="video" />
                    <button type="upload" name="button">Upload Video</button>
                  </vstack>
                </vstack>
              </form>
            </vstack>
          </aside>
        </vstack>
      </vstack>
    </vstack>
  </main>
</body>
{% endblock header_content %}

```

- Add a heading
- Add a dummy instruction paragraph
- Add a form element
- Run and refactor

### Add a form element with a dummy link

- Create a `Form` in `forms.py` as `VideoUploadForm`

```python
from django import forms


class VideoUploadForm(forms.Form):
    video = forms.FileField(
        widget=forms.ClearableFileInput(
            attrs={
                "label": "Choose a file",
                "name": "video_upload",
                "id": "video_upload",
                "multiple": False,
            }
        )
    )
```

- Add a `TextField` with a `TextInput` `Widget`
- Add it to the `context` variable of the `homepage` view function

```python
def homepage(request):
    # Create form object
    form = VideoUploadForm()

    # On data sent via form
    if request.method == "POST":
        lg.debug("Request is post")
        # set form data in form object
        form = VideoUploadForm(request.POST, request.FILES)
        # check form validity
        if form.is_valid():
            lg.debug("Form is valid")
            return render(request, "dummy.html", {})
        else:
            error_message = "Invalid Form:\n" + str(form.errors)
            lg.error(error_message)
            raise Http404(error_message)

    context = {"form": form}
    lg.debug("Rendering homepage")
    return render(request, "homepage.html", context)
```

- Place it in `homepage.html`

```html
{% extends "base.html" %} {% load static %} {% block header_content %}
{{block.super }}
<head>
  <title>OpenCV Masker</title>
</head>
<body>
  <main>
    <vstack spacing="m">
      <vstack spacing="s" stretch="" align-x="center" align-y="center">
        <h1>Welcome to OpenCV Masker</h1>
        <p>Add instructions here</p>
      </vstack>
      <spacer></spacer>
      <vstack spacing="l">
        <vstack spacing="xs">
          <aside class="pa-s">
            <vstack>
              <form
                action="{% url 'homepage' %}"
                method="POST"
                enctype="multipart/form-data"
              >
                {% csrf_token %}
                <vstack spacing="s">
                  <vstack>
                    {{form}}
                    <button type="submit" name="button">Upload Video</button>
                  </vstack>
                </vstack>
              </form>
            </vstack>
          </aside>
        </vstack>
      </vstack>
      <spacer></spacer>
    </vstack>
  </main>
</body>
{% endblock header_content %}

```

- Run and refactor

### Add the videos

- Upload to YouTube and embed

```html
      <spacer></spacer>
      <vstack spacing="xs">
        <aside>
          <dl>
            <vstack>
              <vstack class="pa-s">
                <h3>Input Video sample</h3>
                <p>A sample input video</p>
              </vstack>
              <hr />
              <vstack spacing="m" class="pa-s">
                <vstack align-x="center">
                  <iframe
                    width="640"
                    height="480"
                    src="https://www.youtube.com/embed/zWH5yFCHgoA"
                    frameborder="0"
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                    allowfullscreen
                  ></iframe>
                </vstack>
              </vstack>
            </vstack>
          </dl>
        </aside>
      </vstack>
      <spacer></spacer>
      <vstack spacing="xs">
        <aside>
          <dl>
            <vstack>
              <vstack class="pa-s">
                <h3>Output Video sample</h3>
                <p>A sample output video</p>
              </vstack>
              <hr />
              <vstack spacing="m" class="pa-s">
                <vstack align-x="center">
                  <iframe
                    width="640"
                    height="480"
                    src="https://www.youtube.com/embed/Br0PzOEdTY8"
                    frameborder="0"
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                    allowfullscreen
                  ></iframe>
                </vstack>
              </vstack>
            </vstack>
          </dl>
        </aside>
      </vstack>
      <spacer></spacer>
    </vstack>
  </main>
```

- Run and refactor

### Link the form

- Link the form to render `dummy.html`

```python
# On data sent via form
if request.method == "POST":
    lg.debug("Request is post")
    # set form data in form object
    form = VideoUploadForm(request.POST)
    # check form validity
    if form.is_valid():
        lg.debug("Form is valid")
        return render(request, "dummy.html", {})
```

- Link the form to the actual api view

```html
<form
    action="{% url 'video' %}"
    method="POST"
    enctype="multipart/form-data"
    >
```

### Research how to upload files and use checklists

- Research how to upload files and use checklists
- Create plan for it

## Modify form to upload files

- Change `TextField` to `FileField`
- Add a `ClearableFileInput` widget
- Set attrs
- Run and refactor

```python
class VideoUploadForm(forms.Form):
    video = forms.FileField(
        widget=forms.ClearableFileInput(
            attrs={
                "label": "Choose a file",
                "name": "video_upload",
                "id": "video_upload",
                "multiple": False,
            }
        )
    )
```

- Create validation function `check_validation_file_upload` for file size, extension and type and `pass` in `validators.py`
- Create functions `check_validation_file_upload_size`, `check_validation_file_upload_type`, `check_validation_file_upload_extension` file size, extension and type and `pass`
- Add to `validators` parameter

```python
from opencv_masker.validators import check_validation_file_upload


class VideoUploadForm(forms.Form):
    video = forms.FileField(
        widget=forms.ClearableFileInput(
            attrs={
                "label": "Choose a file",
                "name": "video_upload",
                "id": "video_upload",
                "multiple": False,
            }
        ),
        validators=[check_validation_file_upload],
    )
```

- Add a logging function

```python
import logging
import logging.config
from json import load as jload
from pathlib import Path


def get_logger():
    r"""Return a logger.

    Configure logger lg with config for appLogger from config.json["logging"],
    and return it.
    Might need to configure the log path manually.

    Returns
    -------
    lg
        Logger object.

    Examples
    --------
    Get the logging object and use it to log

    >>> lg = get_logger()
    >>> lg.debug("Form is valid")
    appLogger - 2020-11-05 23:52:35,166-2984-DEBUG-Form is valid
    """
    # Configure logger lg with config for appLogger from config.json["logging"]
    CONFIG_DIR = Path(__file__).resolve().parent.parent.parent.parent
    with open(CONFIG_DIR / "config.json", "r") as f:
        config = jload(f)
        logging.config.dictConfig(config["logging"])
    lg = logging.getLogger("appLogger")
    # lg.debug("This is a debug message")
    return lg
```

- Check validation for file size, type, and extension
- These functions will be used to validate the size and type of file uploaded to the app, and ensure that we are getting only the file we want and not something that will crash the app.

```python
from django.core.exceptions import ValidationError
from django_apps.utils import get_logger
from upload_validator import FileTypeValidator

lg = get_logger()

FILE_SIZES = {
    "2.5MB": 2621440,
    "5MB": 5242880,
    "10MB": 10485760,
    "20MB": 20971520,
    "50MB": 52428800,
    "100MB": 104857600,
    "250MB": 214958080,
    "500MB": 429916160,
}


def check_validation_file_upload_size(file):
    lg.debug("Checking file size")
    lg.debug(f"File size is {str(file.size)}")
    if file.size > FILE_SIZES["50MB"]:
        raise ValidationError(f"File should be less than {FILE_SIZES['50MB']}")


def check_validation_file_upload_type(file):
    lg.debug("Checking file type")
    lg.debug("Checking file extension")
    validator = FileTypeValidator(
        allowed_types=["video/mp4"], allowed_extensions=[".mp4"]
    )
    return validator(file)


def check_validation_file_upload(file):
    lg.debug("Checking file size, type, and extension")
    check_validation_file_upload_size(file)
    check_validation_file_upload_type(file)
```

## Create an API that will take the input video, and return an output video url

- Create a view at an url that takes a request
- It extracts the video from the request and stores it
- It calls the class function with the input video
- It returns the video url

### Main tasks

- Create a view that takes a form request
- Get video from the request and store it if necessary
- Pass it to class `Masker` function `apply_mask`
- Get output video path
- Render a page where it can be downloaded
- Refactor homepage

### Create a view that takes a form request

- Create a view function `video`
- Check  if form is valid
- Add to urls

```python
urlpatterns = [
    path("home/", views.homepage, name="homepage"),
    path("video/", views.video, name="video"),
]
```

- Refactor and run

### Get video from the request and store it if necessary

- Get video from the request and store it
- Create a function `store_file(name: str, path: str, and file: FileType)`

```python
from django.core.files.uploadedfile import TemporaryUploadedFile
from django_apps.utils import get_logger

lg = get_logger()


def store_file(name: str, path: str, file: TemporaryUploadedFile):
    r"""Stores the file sent in a request body.

    Stores the file sent in the request body with a particular name at a
    particular place, defined by the `name` and `path` paramteters.

    Parameters
    ----------
    name : str
        Name of the file.
    path : str
        Path of the storage location.
    file: FileType object
        A python wrapper around a file, sent in a request body.

    Returns
    -------
    None
        Writes the file to a location.

    Raises
    ------
    FileNotFoundError
        When file path doesn't exist.

    Examples
    --------
    These are written in doctest format, and should illustrate how to
    use the function.

    >>> store_file("a.mp4", "", request.FILES['video'])
    """
    file_name = path + name
    try:
        with open(file_name, "wb+") as file_writer:
            for chunk in file.chunks():
                file_writer.write(chunk)
        lg.debug(f"Written file to {file_name}")
    except Exception as e:
        lg.error(str(e))
```

- Create media root directory
- Store file in media root directory
- Add `media/` ROOT directory to `.gitignore`
- Refactor and run

### Get output url

- Get output path and add it to `context`

```python
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django_apps.settings import MEDIA_ROOT
from django_apps.utils import get_logger
from opencv_masker.forms import VideoUploadForm
from opencv_masker.utils import store_file

lg = get_logger()


def homepage(request):
    # Create form object
    form = VideoUploadForm()

    # On data sent via form
    if request.method == "POST":
        lg.debug("Request is post")
        return video(request)

    context = {"form": form}
    lg.debug("Rendering homepage")
    return render(request, "homepage.html", context)


def video(request):
    lg.debug(request)
    # On data sent via form
    if request.method == "POST":
        lg.debug("Request is post")
        # set form data in form object
        form = VideoUploadForm(request.POST, request.FILES)
        # check form validity
        if form.is_valid():
            lg.debug("Form is valid")
            store_file("input_video.mp4", MEDIA_ROOT, request.FILES["video"])
            context = {"video_path": "opencv_masker/django_apps/media/output_video.mp4"}
            return render(request, "dummy.html", context)
        else:
            error_message = "Invalid Form:\n" + str(form.errors)
            lg.error(error_message)
            raise Http404(error_message)
    else:
        raise Http404("Only POST requests are accepted")
```

### Refactor homepage

- Rewrite the video file when homepage renders
- Create utility functions.

```python
def read_binary_file(name: str, path: str) -> bytes:
    r"""Reads the file and returns a binary object.

    This function reads the file with name `name` at path `path` as a
    binary object and returns it.

    Parameters
    ----------
    name : str
        A string that specifies the file name.
    path : str
        A string that represents the path to the object.

    Returns
    -------
    binary_file : bytes
        THe binary representation of the file.

    Raises
    ------
    FileNotFoundError
        When file path doesn't exist.

    Examples
    --------
    Pass a file name and a path to the object.

    >>> print(read_binary_file("a.txt", "/").decode())
    Hello world
    """
    file_name = path + name
    try:
        with open(file_name, "rb+") as file_reader:
            binary_file = file_reader.read()
            return binary_file
    except Exception as e:
        lg.error(str(e))


def write_file_to_files(oname: str, opath: str, names: list, paths: list):
    r"""Overwrite a list of files with one file.

    Overwrite a list of files with names `names` and paths `paths` with a
    single file with name `oname` and path `opath`.

    Parameters
    ----------
    oname : str
        Name of the file that will overwrite the other files.
    opath : str
        Path to the file that will overwrite the other files.
    names : list
        List of names of the files that will be overwritten. Each item should
        be `str`.
    paths : list
        List of paths to the files that will be overwritten. Each item should
        be `str`.

    Returns
    -------
    None

    Raises
    ------
    FileNotFoundError
        When file path doesn't exist.

    Examples
    --------
    Pass the name and path of the file that wiil overwrite the other files.
    Pass a list of names and a list of paths of the files that will be
    overwritten.

    >>> write_file_to_files("a.txt", "/", ["1.txt"], ["/"])
    """

    o_file = read_binary_file(oname, opath)
    for name, path in zip(names, paths):
        file_name = path + name
        try:
            with open(file_name, "wb+") as file_writer:
                file_writer.write(o_file)
                lg.debug(f"Written file to {file_name}")
        except Exception as e:
            lg.error(str(e))
```

- Call function to overwrite the input and output files when the homepage renders.

```python
def homepage(request):
    # Create form object
    form = VideoUploadForm()

    # On data sent via form
    if request.method == "POST":
        lg.debug("Request is post")
        return video(request)

    context = {"form": form}
    lg.debug("Rendering homepage")
    write_file_to_files(
        "sample.mp4",
        MEDIA_ROOT,
        ["input_video.mp4", "output_video.mp4"],
        [MEDIA_ROOT, MEDIA_ROOT],
    )
    return render(request, "homepage.html", context)
```

## Create a class that will mask colors in a video

- Turn the existing code into a class
- Create input, output functions
- Create a mask and replace with background

### Main Tasks

- Create a class `Masker`
- Add an input function that gets the video
- Add an output function that returns a video path
- Add mask related functions
- Add a function to apply mask
- Add video writing functions
- Add docstrings
- Refactor and run on pythonAnywhere

### Create a class `Masker`

- Create a module `masker.py`
- Create a class `Masker`
- Initialize it with `video_path` for input video
- Initialize it with `colors` for `dict` of colors
- Refactor and run

### Add an input function that gets the video

- Create a funtion `apply_mask` that gets the input video, and Colors list and sets it to `video_path` and `colors`
- Refactor and run

### Add an output function that returns a video url

- Create an output function that returns the output path

- Create function `get_video` that returns the path to the video
- Return a path to one of the media videos for now
- Return the return of this function in funtion `apply_mask`
- Refactor and run

```python
import time

import cv2
import numpy as np
from django_apps.settings import MEDIA_ROOT
from django_apps.utils import get_logger

lg = get_logger()

# pylint: disable=no-member


class Masker:
    r"""Class for performing masking functions on an input video.

    This class abstracts away the logic of creating a mask from a color and
    using it to replace the masked region with a mask of the background
    instead.

    The class uses OpenCV functions and logs information as it operates.

    Supported colors:
    ----------
    BLUE

    Attributes
    ----------
    colors : dict
        Dict of color values supported by the class. Contains sub dictionaries
        that hold information needed to create masks of that color.
    output_path : str
        Path to the output video file.

    Parameters
    ----------
    video_path : str
        Path to the input video.

    Methods
    ----------
    apply_mask(video_path: str, colors: list)
        Call this method to apply masks to an input video from a list of
        colors. Colors should be in CAPITAL letters.

    Examples
    --------
    Create a Masker object and call the `apply_mask` method.

    >>> from masker import Masker
    >>> maskr = Masker()
    >>> maskr.apply_mask(MEDIA_ROOT + "video_path.mp4", "BLUE")
    """

    def __init__(self, video_path=""):
        self.colors = {
            "BLUE": {
                "multiple": True,
                "num": 2,
                "ranges": [
                    (np.array([75, 125, 20]), np.array([95, 255, 255])),
                    (np.array([95, 125, 20]), np.array([130, 255, 255])),
                ],
            }
        }
        self.video_path = video_path
        self.output_path = MEDIA_ROOT + "output_video.mp4"
        self.input_colors = []

    def apply_mask(self, video_path: str, colors: list):
        self.video_path = video_path
        for color in colors:
            try:
                self.colors[color]
            except KeyError:
                lg.error(
                    "Couldn't recognise color. Please try with a different color or check the color name entered."
                )
                raise ValueError("Unknown Color")
        self.input_colors = self.input_colors + colors
        return self.get_video()

    def get_video(self):
        self.gen_video()
        return self.output_path
```

### Add mask related functions

- Function `get_colors` to get dict of colors and their ranges

```python
def get_colors(self):
    ranges = []
    for color_name in self.input_colors:
        color = self.colors[color_name]
        if color["multiple"]:
            for i in range(color["num"]):
                ranges.append(color["ranges"][i])
        else:
            ranges.append(color["ranges"])

    return ranges
```

- Function `get_mask` to create and return a mask of a color

```python
def get_mask(self, color_range: tuple, hsv):
    # lg.debug(color_range)
    lower, upper = color_range
    mask = cv2.inRange(hsv, lower, upper)  # pylint: disable=no-member
    return mask
```

- Function `get_masks` to create a list of masks from an input list of colors

```python
def get_masks(self, ranges: list, hsv) -> list:
    masks = []
    for color_range in ranges:
        mask = self.get_mask(color_range, hsv)
        masks.append(mask)
    return masks
```

- Function `refine_mask` to refine masks

```python
def refine_mask(self, mask):

    mask = cv2.morphologyEx(  # pylint: disable=no-member
        mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations=1
    )
    mask = cv2.dilate(  # pylint: disable=no-member
        mask, np.ones((3, 3), np.uint8), iterations=1
    )

    return mask
```

- Refactor and run

### Add video writing functions

- Function `gen_video` to iterate over the video and write it

```python
def gen_video(self):
    ranges = self.get_colors()
    lg.debug(ranges)

    captured_video = cv2.VideoCapture(self.video_path)
    lg.debug(captured_video)
    time.sleep(2)
    shape = (
        int(captured_video.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(captured_video.get(cv2.CAP_PROP_FRAME_HEIGHT)),
    )
    lg.info(f"Dimensions of the video: {shape}")
    # For the first 50 frames, get the video background pixels

    background = 0
    for i in range(50):
        return_value, background = captured_video.read()
        if return_value == False:
            continue

    # Flip the frame array so that we get the pixels mirrored
    background = np.flip(background, axis=1)

    count = 0
    fourcc = cv2.VideoWriter_fourcc(*"MP4V")
    output_writer = cv2.VideoWriter(self.output_path, fourcc, 20.0, shape)

    while captured_video.isOpened():
        return_val, img = captured_video.read()
        if not return_val:
            break
        count += 1
        img = np.flip(img, axis=1)

        # Convert to hsv color range
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # pylint: disable=no-member
        masks = self.get_masks(ranges, hsv)

        mask1 = masks[0]
        # lg.debug(mask1)
        if len(masks) > 1:
            for i in range(1, len(masks)):
                mask1 = mask1 + masks[i]
        # lg.debug(mask1)

        mask1 = self.refine_mask(mask1)
        # lg.debug(mask1)
        inv_mask = cv2.bitwise_not(mask1)
        # lg.debug(inv_mask)

        res1 = cv2.bitwise_and(background, background, mask=mask1)
        res2 = cv2.bitwise_and(img, img, mask=inv_mask)
        final_output = cv2.addWeighted(res1, 1, res2, 1, 0)

        output_writer.write(final_output)

    lg.info(f"Wrote frames: {count}")
```

- Refactor and run

### Add more colors

- Add `RED` color to `colors` dict

```python
self.colors = {
    "BLUE": {
        "multiple": True,
        "num": 2,
        "ranges": [
            (np.array([75, 125, 20]), np.array([95, 255, 255])),
            (np.array([95, 125, 20]), np.array([130, 255, 255])),
        ],
    },
    "RED": {
        "multiple": True,
        "num": 2,
        "ranges": [
            (np.array([100, 40, 40]), np.array([100, 255, 255])),
            (np.array([155, 40, 40]), np.array([180, 255, 255])),
        ],
    },
}
```

### Refactor the class

- The class doesn't seem to work.
- Rather than find the bug, refactor it into fewer methods.

## Create a view that returns the video in a page

- Create a video page that displays the video

### Main tasks

- Create a view and url to display the video with context
- Create a template to display the video
- Show warning to download or video will disappear

### Create a view and url to display the video with context

- Create a view `show_video` to display the video

```python
def show_video(request):
    lg.debug(request)

    context = {"filename": "output_video.mp4"}
    return render(request, "show_video.html", context)
```

- Create a `context` dict with url of the output video
- Add url as `show_video/`

```python
path("show_video/", views.show_video, name="show_video"),
```

## Create a template to display the video

- Create a template `show_video.html`

```html
{% extends "base.html" %} {% load static %} {% block header_content %}
{{block.super }}
<head>
  <title>OpenCV Masker</title>
</head>
<body>
  <main>
    <vstack spacing="m">
      <vstack spacing="s" stretch="" align-x="center" align-y="center">
        <h1>Download the Masked Video</h1>
        <p>
          Save the video by downloading it. To save memory, it will soon be
          deleted and overwritten.
        </p>
      </vstack>
      <spacer></spacer>
      <vstack spacing="xs">
        <aside>
          <dl>
            <vstack>
              <vstack class="pa-s">
                <h3>Download video</h3>
                <p>Save video or it will be deleted</p>
              </vstack>
              <hr />
              <vstack spacing="m" class="pa-s">
                <vstack align-x="center">
                  <button type="download" name="download_button">
                    <a href="{% url 'download' filename %}"
                      ><h2>Download Video</h2></a
                    >
                  </button>
                </vstack>
              </vstack>
            </vstack>
          </dl>
        </aside>
      </vstack>
      <spacer></spacer>
    </vstack>
  </main>
</body>
{% endblock header_content %}

```

- Add a heading
- Add elements to display output video
- Research downloading of the video
- Create a `download` view

```python
def download(request, filename):
    lg.debug(request)
    try:

        filepath = MEDIA_ROOT + filename
        lg.info(f"Setting up {filename} for download at {filepath}")

        response = FileResponse(
            open(filepath, "rb+"), as_attachment=True, filename=filename
        )
        return response
    except Exception as e:
        lg.error(e)
        return Http404("File download error")
```

- Add url as `"download/<str:filename>/"`

```python
path("download/<str:filename>/", views.download, name="download"),
```

- Return `filename` in context
- Create a `filepath` with `MEDIA_ROOT` + `filename`
- Create a `FileResponse` object and return it
- If there is an exception, return `404`
- Show a button that will start download of the video and put the URL inside it.
- Refactor and run

### Show warning to download or video will disappear

- Add text that says `Save video or it will be deleted`

### Pass it to class `Masker` function `apply_mask`

- Call `Masker.apply_mask` with video path
- Redirect to `show_video`

```python
masker = Masker()
masker.apply_mask(MEDIA_ROOT + "input_video.mp4", ["BLUE"])
return HttpResponseRedirect("/masker/show_video/")
```

- Refactor and run

## Add a form check list with `blue` and `red` on it

- Research how to dropdown list to a django form
- Add `RED` and `BLUE` to it
- Create a tuple `colors` of choices from colors list in `Masker.colors`
- Create a `ChoiceField` `color` and pass `colors` to it.
- Run and refactor

```python
masker = Masker()
colors = masker.colors.keys()
colors = tuple([(color, color) for color in colors])


class VideoUploadForm(forms.Form):
    video = forms.FileField(
        widget=forms.ClearableFileInput(
            attrs={
                "label": "Choose a file",
                "name": "video_upload",
                "id": "video_upload",
                "multiple": False,
            }
        ),
        validators=[check_validation_file_upload],
    )
    color = forms.ChoiceField(choices=colors)
```

## Refactor `views.video` to call `Masker.apply_mask` with color in form

- Get the color value from the form
- Turn it into a list and pass it to `Masker.apply_mask`
- Run and refactor

```python
color = form.cleaned_data["color"]
lg.info(f"Color selected: {color}")
```

## Additional Information

### Screenshots

### Links

## Notes template

```python
```

```html

```
