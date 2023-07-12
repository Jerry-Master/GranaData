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
version: "3"

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

You will need to substitute `myuser` and `mydatabase` with what you like most. To explain a bit what is happening here, we are running a postgres container, then performing healthy checks to be sure the database is running and after that we launch the webapp container. You could provide the password also there, but for security reasons is better to provide it through an environment variable, just like before. The database is stored in the folder `postgres_data` locally, so that whenever you kill the container you don't lose the data. The port 5432 is forwarded locally so you can connect to the database from your machine when the container is running and see the data.

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

Amazon Web Services are a way to deploy your code into servers that you don't need to manage. This way instead of the cost of setting up a whole server, you just pay for the hours used. Nevertheless, you won't save yourself the cost of configuring everything. Even though configuring AWS may be simpler than configuring a server, it is still an important investment of time. For that, I will provide here the bare minimum to make our webapp work on AWS. You will still need to read the AWS docs extensively, there are many tutorials online, but Amazon keeps changing the interface every so often. The only web that is for sure updated is the [AWS official docs page](https://docs.aws.amazon.com/){:target="_blank"}.

## Account and IAM roles

Before we can start configuring the server, we need to configure an account. For that you will need access keys. You can create access keys for your root account but it is not recommended. AWS recommends that you create role with less permissions than your root account (specially without billing permissions) and to use those access keys. In the past this was made using the Identity and Access Management (IAM) app. Now, it is being migrated to IAM Identity Center. Both methods still work as of this writing but I will explain the second one which is more updated. The following is a reduced version of [this tutorial](https://docs.aws.amazon.com/singlesignon/latest/userguide/getting-started.html){:target="_blank"}. Go to the [AWS console](https://console.aws.amazon.com/){:target="_blank"}. There look for the IAM Identity Center. Once on the IAM Identity Center you will need to create an user, create a permission set and link both. In the section User click to Add User and fill the neccesary information. Then, on permission sets, click on Create permission set and create the predefined role AdministratorAccess. After that, go to AWS accounts, select the account under root and click Assign users or groups. Select your created user, click next, select the role, click next, review it and click submit. Finally, to activate that user, you must open the mail you provided and register that user with some password. Before you continue, go to Dashboard and save your AWS access portal URL, that is the URL you need to use to log in with that user. Now, click that URL and sign in. Once you are logged in you should see your user and two links at the right: one for Management console and one for Command line or programatic access. Click the latter and you will see your access keys.

The next step is to install and configure the AWS CLI. Go [here](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html){:target="_blank"} and follow the steps for the installation. Once installed execute `aws configure` and provide the access key and secret access key obtained previously. It will also ask for a region, I will be using `us-east-1`. If you choose a different one you may encounter problems later on because the free tiers differ across regions. And for the output format choose `json`. You are now (almost) ready to start launching instances.


## EC2 Instances

Having created our account it is time to create an instance where to deploy our webapp. If your page gets too large you may be interested in storing the database in S3 buckets, but for now I will store code and data in the same instance. You can find the docs for EC2 [here](https://docs.aws.amazon.com/ec2/index.html){:target="_blank"}. As before, I will summarize it to just use what we need. First, create the instance. For that go to the [EC2 console](https://us-east-1.console.aws.amazon.com/ec2){:target="_blank"}. Under Instances section, click Launch instances. There give it a name, select the OS and arch (I recommend Ubuntu and x86-64), select the instance type (I will be using t2.micro cuase it is free), select a key-pair or create since you probably don't have one and leave everything as default. Once you launched it you can now access your machine through ssh. In the instances section, you can click on your created instance and then click on Connect and it will give you instructions on how to connect. The next steps are to install Docker, copy your webapp to the instance, change the firewall of the instance to allow http and postgres traffic and finally deploy the app. 

### Installing Docker (again)

If you have chosen Ubuntu as your OS you can follow the instructions [here](https://docs.docker.com/engine/install/ubuntu/){:target="_blank"}. You just basically need to execute the following commands after accessing the machine:

```bash
sudo apt-get update -y
sudo apt-get install ca-certificates curl gnupg -y
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update -y
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y
```

And if you want to check that everything is working just do

```bash
sudo docker run hello-world
```

### Upload your code to EC2

You can copy your entire directory recursively into you EC2 instance with scp:

```bash
scp -r -i YOUR_KEY ./* ubuntu@YOUR_EC2_ADDRESS:.
```

`YOUR_KEY` is the key pair previously created and `YOUR_EC2_ADDRESS` may look something like `ec2-30-29-46-221.compute-1.amazonaws.com`. It is the same address that you use to ssh into your machine.

### Changing the firewall

In AWS, the instances have some security rules that control the inbound and outbound traffic of your app. By default all the ports are closed except for 22 which is the ssh port. We will need to open the port 80 and 5432 since they are the http and postgres ports. If you have an SSL certificate you could open the port 443 for https, but we will just use those two for now. Let's go back to the [EC2 console](https://us-east-1.console.aws.amazon.com/ec2){:target="_blank"} and go to Security Groups. Click on Create security group. Give it a name and add two inbound rules. You can just select HTTP and Postgresql in the dropdown menu and it will set the port for you automatically. Then, on source, select Anywhere IPv4 and click Create security group. Now go back to your created instance and click Actions > Security > Change security groups. There simply add the newly created security group and you are free to go.

## Deploy the app

In order to deploy our app we need to make one change to our `docker-compose.yml`. Initially we were redirecting port 8000 into 8000, we are now going to redirect it to 80 which the http port. The line to change will end up like this

```txt
ports:
  - 80:8000
```

Finally, ssh into your machine with docker installed and execute

```bash
sudo DB_PASSWORD=... docker compose up -d
```

Remember that you have to specify the password of the database as a environment variable. Okay, the app is running but, how can we access it? Well, we cannot. We still need to make some changes. Stop the container and let's finish this:

```bash
sudo DB_PASSWORD=... docker compose down
```

The first thing to know is what is the IP that we can use to access this page. In the AWS console, when you enter your instance it displays somewhere "Public IPv4 address". That is the IP of your app. However, if you were to enter there, Django will not let you in. That is because you need to allow that host. For that, go the `setting.py` of your app and add it:

```python
ALLOWED_HOSTS = ['YOUR_IP']
```

Also, even after changing this, when you access your ip you don't see the page. That is because the base url is not pointing anywhere, but we can fix that. Create a view that only has the redirection:

```python
from django.shortcuts import redirect

def redirect_to_create_user(request):
    return redirect('/simpleapp/create_user')
```

Then, in your main `urls.py` add `path('', redirect_to_create_user)`, it will end up like this:

```python
from django.contrib import admin
from django.urls import path
from django.urls import include
from .views import redirect_to_create_user

urlpatterns = [
    path('', redirect_to_create_user),
    path('admin/', admin.site.urls),
    path('simpleapp/', include('simpleapp.urls')),
]
```

Now, copy again all the files into your machine and deploy the webapp:

```bash
sudo DB_PASSWORD=... docker compose up -d
```

### Accessing the DataBase

Let's see how we can access the server database locally. Open you favourite DB program (mine is DBeaver) and create a new connection. This time you will have to provide an URL instead of localhost. Everything else is the same as when you did it locally. The port is 5432, the user is what you gave it, and the database name is what you name it. If you have configured properly the EC2 security group you could now access your database locally.

# Web Domain

Nice, we have our fantastic webapp up and running, but wait, are you going to share to your friends the page 50.283.48.100? Obviously not, you need a fancy domain like myawesomepage.com or something that describes your project. To achieve that you need to first buy a domain and then link that domain to your IP. Domains that are not on high demand typically cost around 10$ to 20$. You can buy them on [Namecheap](https://www.namecheap.com/){:target="_blank"}. Once you have it you need to do several things on the AWS side. You will need to fix the IP so that it doesn't change, otherwise the DNS redirection will get broken over time. After that you need to create nameservers and then route your domain to that IP. Let's go step by step. To fix the IP go to the section Elastic IP in the left bar of the EC2 menu. Create such Elastic IP and then, in actions, associate it to your instance. Once you have done that, you will need to create the hosted zone. For that, search in AWS the Route 53 service. Once there, click on Create hosted zone. Insert your domain and create it. Before we continue, two more records need to be created. Create one with Type A and your previous Elastic IP under the value section, everything else as default. Repeat now but add 'www' in subdomain so that your page can be accessed either by its domain or adding www at the beginning. Once you have done that, go to your domain on Namecheap and click on manage. Select custom DNS and enter the four nameservers that were created previously. If you didn't understand something, you can check the tutorials I followed both for [the AWS](https://techgenix.com/namecheap-aws-ec2-linux/){:target="_blank"} and [Namecheap part](https://www.namecheap.com/support/knowledgebase/article.aspx/10371/2208/how-do-i-link-my-domain-to-amazon-web-services/){:target="_blank"}. DNS redirection may take up to 48 hours. Wait for it, and you will have your marvelous webpage running.