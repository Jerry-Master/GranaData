---
layout: post
title:  "Deploying AWS webapp tutorial"
author: jose
categories: [ Django, Docker, AWS ]
featured: false
hidden: false
comments: false
share: false
use_math: false
image: null
time_read: -1
---

Following the philosophy of my blog, this will be a very specific post. You can find many resources on the internet about how to deploy a web app.
I will even be referencing many of those here. But the main difference with those posts is that mine is going to be straight to the point.
The following is a tutorial on how to create a web app from scratch. The backend will be on Django and the database will be Postgresql.
The app will be running on AWS and to deploy it there we will create a Docker image. Last but not least, I'll explain how to buy a domain and link the domain to the AWS ip address. Let's get ours hands dirty!


## Django and Postgresql

Let's start by creating a minimal python environment with just Django. You can do it either via python or conda. For reproducibility, please use python3.10 and Django 4.2.2. Open a terminal and run the following:

```bash
python3.10 -m venv .venv
source .venv/bin/activate # For Windows use: .\.venv\Script\activate
pip install django==4.2.2 psycopg2-binary
```

For the Conda installation:

```bash
conda create --name .venv python=3.10
conda activate .venv
pip install django==4.2.2 psycopg2-binary
```

### Postgresql server setup

The next step is to create a prosgresql server. To install postgresql go to the [official page](https://www.postgresql.org/download/){:target="_blank"}. Once installed, you need to start running the server on your system:

```bash
mkdir /usr/local/var/postgres  # Create folder if it does not exist
initdb -D /usr/local/var/postgres  # Initialize database cluster
pg_ctl -D /usr/local/var/postgres start  # Start server
```

This will start the server and save everything into the `/usr/local/var/postgres` folder. For Window users, replace `pg_ctl` and `initdb` with the path to the `pg_ctl.exe` and `initdb.exe` binaries, which may be something similar to `"C:\Program Files\PostgreSQL\14\bin\pg_ctl.exe"` and use any data directory you want.

Once the server is running we need to create a database, for that, you need to run postgres in a terminal and execute the relevant SQL code:

```bash
psql postgres  # Start SQL shell
postgres=# CREATE DATABASE mydatabase;
postgres=# CREATE USER myuser WITH PASSWORD 'mypassword';
postgres=# GRANT ALL PRIVILEGES ON DATABASE mydatabase TO myuser;
postgres=# exit;
```

The commands are self-explanatory, just replace `mydatabase`, `myuser` and `mypassword` with what you deem appropiate. Now you have the database ready to use locally, you can connect to it using any database management system you want, I recommend [Dbeaver](https://dbeaver.io/download/){:target="_blank"}. The connection is through localhost and port 5432. Later on we will see how to automate this process but for now, this is how it is done locally.

### Django webapp setup

Given the database, we need a web on top. With the python environment activated, run the following using any name you want:

```bash
django-admin startproject myprojectname
```

This will create the basic skeleton for a Django project. We now have to configure the database and create a simple app to store data. Go to `settings.py` and locate the {% ihighlight python %}INSTALLED_APPS{% endihighlight %} variable. Append {% ihighlight python %}'django.db.backends.postgresql',{% endihighlight %} to the list, it should be like this:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.db.backends.postgresql',
]
```

Also locate the {% ihighlight python %}DATABASES{% endihighlight %} variable and modify it to contain the information necessary to connect to the posgresql database:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydatabase',
        'USER': 'myuser',
        'PASSWORD': 'mypassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

Since storing passwords in plain text is normally not a good idea, I recommend you use environment variables for that:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydatabase',
        'USER': 'myuser',
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),  # Don't forget to import os
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

You can now provide the password through environment variables:

```bash
export DB_PASSWORD='mypassword'  # Unix
set DB_PASSWORD "mypassword"  # CMD Windows
$env:DB_PASSWORD="mypassword"  # PowerShell Windows
```

Finally, let's create a simple page. Start by typing:

```bash
python manage.py startapp simpleapp
```

Now, modify `settings.py` to include it by adding it to the {% ihighlight python %}INSTALLED_APPS{% endihighlight %} variable:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.db.backends.postgresql',
    'simpleapp',
]
```

After that, we will add a very simple model and view to handle data. Our model will only contain names of users. Go to `simpleapp/models.py` and add this:

```python
class User(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
```

Then, create `simpleapp/forms.py` and add this:

```python
from django import forms
from .models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name']
```

Next, modify `simpleapp/views.py` to include the following:

```python
from django.views.generic.edit import CreateView
from .models import User
from .forms import UserForm

class UserCreateView(CreateView):
    model = User
    form_class = UserForm
    template_name = 'user_form.html'
    success_url = '/create_user
```

You also need to create the template under a templates folder, create `simpleapp/templates/user_form.html` and insert this:

```html
<form method="post">
    {% raw %}{% csrf_token %}{% endraw %}
    {% raw %}{{ form.as_p }}{% endraw %}
    <button type="submit">Create</button>
</form>
```

Last, we need to link the urls for everything to work properly. Create the file `simpleapp/urls.py` and write:

```python
from django.urls import path
from .views import UserCreateView

urlpatterns = [
    path('create_user/', UserCreateView.as_view(), name='create_user'),
]
```

Go to the main `myprojectname/urls.py` and edit it to be like this:

```python
from django.contrib import admin
from django.urls import path
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('simpleapp/', include('simpleapp.urls')),
]
```

Now you are good to go. We can finally start adding rows to the database. For doing so, apply migrations and start the webapp:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Open a browser, go to `http://127.0.0.1:8000/simpleapp/create_user/` and you will be able to input users' names. If it is your first time using Django, this is a whole lot, I know. This is a simple example using Django's class-based views. Things can get very, very complex. The aim of this tutorial is to set up a minimal working webapp. For more information on Django, you can go to their [official documentation](https://docs.djangoproject.com/en/4.2/){:target="_blank"}. Okay, close everything and let's start our Docker journey. To stop the webapp run `ctrl+C` and to stop the posgresql server run:

```bash
pg_ctl -D /usr/local/var/postgres stop
```

## Docker


## AWS

### Account and IAM roles

### ECS cluster setup


## Web Domain