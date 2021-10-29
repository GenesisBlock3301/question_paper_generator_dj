from django.urls import path,include
from . import views
urlpatterns = [
    path("", views.test,name="test"),
    path("login/", views.LoginView.as_view(),name="login"),
    path("register/", views.RegistrationView.as_view(),name="register"),
]
