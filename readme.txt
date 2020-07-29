Django Routes for the project:
http://localhost:8000/client
http://localhost:8000/client/new
http://localhost:8000/client/1  - consult
http://localhost:8000/client/1/edit
http://localhost:8000/client/1/delete
http://localhost:8000/test - test page

REST Api(without Django Rest Framework):
http://localhost:8000/clients                    HTTP GET         - get all clients
http://localhost:8000/clients/new                HTTP GET/POST    - create client
http://localhost:8000/clients/1                  HTTP GET         - consult client
http://localhost:8000/clients/1/edit             HTTP GET/POST    - edit client
http://localhost:8000/clients/1/delete           HTTP GET/DELETE  - delete client

REST Api with Django Rest Framework:
http://localhost:8000/api/clients                    HTTP GET         - get all clients
http://localhost:8000/api/clients                    HTTP POST        - create client
http://localhost:8000/api/clients/1                  HTTP GET         - consult client
http://localhost:8000/api/clients/1/                 HTTP PUT         - edit client
http://localhost:8000/api/clients/1/                 HTTP DELETE      - delete client

Making the project:
Using Django, SQLAlchemy (mapping) and Sqlite (embedded database) Python packages

List environemments:
conda env list

#Create a conda Environment for the project(ex: SampleDjango, version python >= 3). First with command promt go to d:\python\examples\
conda create -n SampleDjango python=3
conda activate SampleDjango
conda deactivate

Install the latest Django release(from the new environment and from the new folder):
(SampleDjango) d:\python\examples>python -m pip install django
conda list

Create a Django project(django-admin is installed inside the new virtual environement)
(SampleDjango) d:\python\examples> django-admin startproject SampleDjango

Move into the projet directory:
>cd SampleDjango

Run the developement server:
(SampleDjango) d:\python\examples\SampleDjango>python manage.py runserver
Starting dev server at: http://127.0.0.1:8000/

Run the initial migrations(admin and auth). From the created environment and the project folder run:
>python manage.py showmigrations 
>python manage.py sqlmigrate clients 0001 - generate the SQL for migration 
>python manage.py migrate  

Most Djange projects contains several apps (app=it's a python package or component). It contains models, view, templates, urls..

Create a django app named 'clients'
(SampleDjango) d:\python\examples\SampleDjango> python manage.py startapp clients
Add a view function:
  Edit views.py in 'clients' folder and add a view function:
  def welcome(request):
    return HttpResponse("Welcome to Django! ")
Assign a URL to the view function
  Open urls.py in SampleDjango subfolder(core folder for the projects) and add a url: path('test', welcome) in urlpatterns = []
Run a view the page
(SampleDjango) d:\python\examples\SampleDjango>python manage.py runserver
Then: http://127.0.0.1:8000/test

Add the Adresse, Client and Commande model in models.py in 'clients' app
>python manage.py makemigrations 
>python manage.py migrate 

Edit settings.py in SampleDjango subfolder(core folder for the project) and add 'clients' in the list: INSTALLED_APPS = []

Model Template View(MTV) pattern = MVC pattern(Template = component  to display data to the user)
Create a subfolder templates\app in every app(ex templates\clients for clients app and copy the client templates)

Check the database with dbshell command:
>python manage.py dbshell
sqlite> .tables
sqlite> select * from django_migrations;
sqlite> select * from clients_client;
sqlite> .exit
or
Command Line Shell For SQLite
SampleFlask>sqlite3
sqlite>.open db.sqlite3
sqlite>.tables
sqlite>select * from clients_client;
sqlite>.exit

Admin interface to create and edit model data
1.Register model with admin site
   Edit admin.py in clients app with this:  from .models import Adresse, Client, Commande
                                            admin.site.register(Client)
2.Configure superuser
>python manage.py createsuperuser
admin info@example.com admin
then go to: http://127.0.0.1:8000/admin

Otherwise, export/Import data from JSON File(from app/fixtures directory):
>python manage.py dumpdata --format=json --indent 2 clients > clients/fixtures/save-data.json
Load initial data:
>python manage.py loaddata init-data.json
    
Others: 
1.Django Rest Framework for simple REST Api web interface
Install the djangorestframework package: >conda install -c conda-forge djangorestframework
Add also'rest_framework'(Django Rest Framework) in project INSTALLED_APPS = []
Add serializers.py file, modify views.py (add class ClientViewSet), add router dans urls.py (in 'clients' app folder)
Acces via browsable API:
http://localhost:8000/api/

2.Django Widget Tweaks for using render_field template tag(to link the input tag to the form field(forms.py) with particular CSS styles) in client_fiche.html template
install django-widget-tweaks(to add classed to the form fields)
conda install -c conda-forge django-widget-tweaks
add ‘widget_tweaks’ to INSTALLED_APPS.
    

Git: A new repo from an existing project
git init
git add clients/* SampleDjango/* 
git add manage.py db.sqlite3 readme.txt
git commit -m "first commit"
Connect it to github ad create a new repository: SampleDjango
git remote add origin https://github.com/danielvornicu/SampleDjango.git
git push -u origin master



Deploy SampleDjango application on Heroku with Heroku CLI:
Set a certificate if necessary:
>set NODE_EXTRA_CA_CERTS=d:\python\examples\heroku\Certificat.cer

Make a requirements.txt in SampleDjango project folder file with:
django>=3.0.7
django-widget-tweaks>=1.4.5
djangorestframework>=3.11.00
gunicorn==20.0.4
whitenoise==5.1.0

then Procfile:
web: gunicorn SampleDjango.wsgi

Use WhiteNoise with Django for simplified static file serving:
Modify: SampleDjango/settings.py adding:
1.Make sure staticfiles is configured correctly
  STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')      
2.Enable WhiteNoise:
  MIDDLEWARE = [
      ...
      'whitenoise.middleware.WhiteNoiseMiddleware',
  ]
3.Add compression and caching support
  STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
4. Add the host in ALLOWED_HOSTS:
  ALLOWED_HOSTS = [
       'floating-river-31233.herokuapp.com'
  ]  
  
an add them to git:
git add requirements.txt Procfile SampleDjango/settings.py
git commit -m "3 files added"
git push -u origin master

>heroku create
>heroku buildpacks:set heroku/python --app floating-river-31233
>heroku config:set DISABLE_COLLECTSTATIC=1
>git push heroku master

Then go to:
https://floating-river-31233.herokuapp.com/client/
