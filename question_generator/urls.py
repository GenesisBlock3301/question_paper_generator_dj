from django.urls import path,include
from . import views

urlpatterns = [
    path("", views.LandingView.as_view(),name="landing"),
    path("faculty/", views.FacultyView.as_view(),name="faculty"),
    path("department/", views.DepartmentView.as_view(),name="department"),
    path("courses/", views.CoursesView.as_view(),name="course"),
    path("uquestions/",views.UserQuestionView.as_view(),name="uquestions"),
    path("questions/",views.QuestionsView.as_view(),name="questions"),
    path("pquestions/",views.PendingQuestionView.as_view(),name="pquestions"),
    path("question/<id>/",views.SingleQuestionView.as_view(),name="question"),
    path("create-question/", views.CreateQuestion.as_view(),name="create-question"),
    path("update/<pk>/", views.UpdateQuestionView.as_view(),name="update-question"),
    path("<pk>/delete",views.DeleteQuestionView.as_view(),name="delete-question"),
    path("<pk>/delete",views.DeleteQuestionView.as_view(),name="delete-question"),
    path('ajax/load-course/', views.load_course, name='ajax_load_course'), 
    path("approval/<pk>/",views.question_approval,name="approval"),

    path("faculty-question/<faculty>/", views.FacultyQuestionView.as_view(), name="faculty-question"),
    path("dept-question/<dept>/", views.DepartmentQuestionView.as_view(), name="dept-question"),
    path("course-question/<course>/", views.CourseQuestionView.as_view(), name="course-question"),
    # path('table/', views.DataTableView.as_view(), name='table'), 
    
]
