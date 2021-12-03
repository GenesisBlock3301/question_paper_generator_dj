from django.urls import path,include
from . import views

urlpatterns = [
    path("", views.LandingView.as_view(),name="landing"),
    path("faculty/", views.FacultyView.as_view(),name="faculty"),
    path("department/", views.DepartmentView.as_view(),name="department"),
    path("course/", views.CourseView.as_view(),name="course"),
    path("uquestions/",views.UserQuestionView.as_view(),name="uquestions"),
    path("questions/",views.QuestionsView.as_view(),name="questions"),
    path("pquestions/",views.PendingQuestionView.as_view(),name="pquestions"),
    path("question/<id>/",views.SingleQuestionView.as_view(),name="question"),
    path("create-question/", views.CreateQuestion.as_view(),name="create-question"),
    path('ajax/load-course/', views.load_course, name='ajax_load_course'), 
    # path('table/', views.DataTableView.as_view(), name='table'), 
    
]
