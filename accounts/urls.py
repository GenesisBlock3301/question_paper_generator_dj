from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.LoginView.as_view(),name="login"),
    path("register/", views.RegistrationView.as_view(),name="register"),
    path("aregister/", views.AdminRegistrationView.as_view(),name="aregister"),
    path("create-profile/",views.CreateTeacherProfile.as_view(),name="create-profile"),
    path("profile/",views.TeacherProfile.as_view(),name="teacher-profile"),
    path("teachers/",views.TeacherList.as_view(),name="teachers"),
    path("teacher-admin-view/<pk>/",views.TeacherProfileShowAdmin.as_view(),name="teachers-admin"),
]
