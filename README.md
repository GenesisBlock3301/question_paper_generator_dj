
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