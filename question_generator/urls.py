from django.urls import path,include
from . import views

urlpatterns = [
    path("landing/", views.LandingView.as_view(),name="landing"),
    path("faculty/", views.FacultyView.as_view(),name="faculty"),
    path("department/", views.DepartmentView.as_view(),name="department"),
    path("course/", views.CourseView.as_view(),name="course"),
    path("create-question/", views.CreateQuestion.as_view(),name="create-question"),
    path('ajax/load-course/', views.load_course, name='ajax_load_course'), 
    
]
