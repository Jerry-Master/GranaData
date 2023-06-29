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
The app will be running on AWS and to deploy it there we will create a Docker image. Last but not least, I'll explain how to buy a domain and link the domain to the AWS ip address. Let's get ours hands dirty! Also, don't worry about the code, it is all available [here](https://github.com/Jerry-Master/GranaData/tree/main/_code/django_docker_aws){:target="_blank"}.


# Django and Postgresql

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

## Postgresql server setup

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

## Django webapp setup

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

# Docker

Setting everything from scratch is time consuming but if you only need to do it once, it is affordable. The problem comes when you want to migrate to other machines or you want to scale. Having to go through all the process above everytime is annoying. As I mentioned before, it would be nice to automate it. That's when Docker comes into play. It is a way to pack everything up so that it can run on your machine, the cloud or a microwave, if it has Docker installed, of course. A Docker is basically made of a few configuration files that are used to construct an image that does whatever you want, in our case handle data through a web app. Having introduced the concept, let's build a Docker for our web app.

This section is mostly inspired by [this other tutorial](https://learndjango.com/tutorials/django-docker-and-postgresql-tutorial){:target="_blank"}. Hand over there if you feel curious. Also, I recommend you giving a look at the [official Docker beginner tutorial](https://docker-curriculum.com/){:target="_blank"} for more information on how to set up Docker and the basics of it.

To start, create a Dockerfile inside of the Django project directory. Specify the following information on it:

```dockerfile
FROM python:3.10.2-slim-bullseye

WORKDIR /code

COPY . .
RUN pip install -r requirements.txt
```

You also need to create a `requirements.txt` with this:

```txt
django==4.2.2
psycopg2-binary
```

You could simply install it with pip, but when the project grows you will be thankfull to have it all in a `requirements.txt` file. So, that's the container of the webapp. Simple, right? However, we still need to connect it to a posgres database. For that we need to use docker compose to run another container with the database and connect them. For that, create a `docker-compose.yml` file with the following:

```txt
version: "3.9"

services:
  web:
    build: .
    command: sh start.sh
    environment:
      - DB_PASSWORD
    volumes:
      - .:/code
    ports:
      - 8000:8000
    depends_on:
      db:
        condition: service_healthy
  db:
    image: postgres:14
    restart: always
    ports:
      - 5432:5432
    environment:
      POSTGRES_DB: mydatabase
      POSTGRES_USER: myuser
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - ./postgres_data:/var/lib/postgresql/data/
    healthcheck:
      test: pg_isready -U myuser -d mydatabase
      interval: 1s
      timeout: 10s
      retries: 10
      start_period: 30s
```

You will need to substiture `myuser` and `mydatabase` with what you like most. To explain a bit what is happening here, we are running a postgres container, then performing healthy checks to be sure the database is running and after that we launch the webapp container. You could provide the password also there, but for security reasons is better to provide it through an environment variable, just like before. The database is stored in the folder `postgres_data` locally, so that whenever you kill the container you don't lose the data. The port 5432 is forwarded locally so you can connect to the database from your machine when the container is running and see the data.

Wait! We have not finished yet. We need to create the `start.sh` and modify the `myprojectname/settings.py` file. The `DATABASES` variable should look like this:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydatabase',
        'USER': 'myuser',
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': 'db',
        'PORT': '5432',
    }
}
```

The only change is on `HOST`. It is now set up to `db` which is the name of the posgres container. And the `start.sh` script is the following:

```python
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

It is creating all the migrations needed to set up all the models from Django into postgres. Finally, just run the container:

```bash
docker compose up
```

To stop it, do `ctrl+C` and then `docker compose rm`. That's it, that's all you need to do to restart your webapp from anywhere. You can now take your code to any machine and you won't need to set up posgres, python and django from scratch. Just install docker and run `docker compose up`. Also, it is a good practice to include a `.dockerignore`, just like `.gitignore`. For this simple app I have

```txt
postgres_data/
Dockerfile
docker-compose.yml
*/__pycache__/
*/*/__pycache__/
*/*/*/__pycache__/
```

This way I don't load any unnecessary files to the container, making it faster. So now that we have everything packed up in our bag, let's travel. Let's deploy the web to AWS for others to use it.

# AWS

## Account and IAM roles

## ECS cluster setup


# Web Domain