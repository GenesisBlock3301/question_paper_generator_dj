from django.urls import path
from . import views

urlpatterns = [
    path("tlogin/", views.TeacherLoginView.as_view(),name="tlogin"),
    path("alogin/", views.AdminLoginView.as_view(),name="alogin"),
    path("tregister/", views.TeacherRegistrationView.as_view(),name="tregister"),
    path("aregister/", views.AdminRegistrationView.as_view(),name="aregister"),
    path("create-profile/",views.CreateTeacherProfile.as_view(),name="create-profile"),
    path("update-profile/<pk>/",views.UpdateTeacherProfileView.as_view(),name="update-profile"),
    path("profile/",views.TeacherProfile.as_view(),name="teacher-profile"),
    path("teachers/",views.TeacherList.as_view(),name="teachers"),
    path("logout/",views.logout_view,name="logout"),
    path("teacher-admin-view/<str:email>/",views.TeacherProfileShowAdmin.as_view(),name="teachers-admin-view"),
]
