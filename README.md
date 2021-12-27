
# ENV setup

Env creation inside project folder:
```
python -m venv env
```
Active env:
```
source env/bin/activate
pip install django
```


# Django project setup:

Create django project:
```
django-admin startproject project
```
Create django app:

```
python manage.py startapp app_name
```
DataFlow of Django:
```
Template(browser) -> urls -> view <- database
```

# Project Run
step 1: Project migration
way 1:
```
python manage.py  makemigrations 
python manage.py  migrate
```
way 2:
```
python manage.py makemigrations app_name
python manage.py migrate app_name

must:
python manage.py migrate
```
step 2:
Run project:
```
python3 manage.py runserver
```

