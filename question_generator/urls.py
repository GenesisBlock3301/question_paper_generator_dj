from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.LandingView.as_view(), name="landing"),
    path("faculty/", views.FacultyView.as_view(), name="faculty"),
    path("department/", views.DepartmentView.as_view(), name="department"),
    path("courses/", views.CoursesView.as_view(), name="course"),
    path("tquestions/", views.TeacherQuestionView.as_view(), name="tquestions"),
    path("tpquestions/", views.TeacherPendingQuestionView.as_view(),
         name="tpquestions"),
    path("questions/", views.QuestionsView.as_view(), name="questions"),
    path("pquestions/", views.PendingQuestionView.as_view(), name="pquestions"),
    path("question/<id>/", views.SingleQuestionView.as_view(), name="question"),
    path("create-question/", views.CreateQuestion.as_view(), name="create-question"),
    path("update/<pk>/", views.UpdateQuestionView.as_view(), name="update-question"),
    path("<pk>/delete", views.DeleteQuestionView.as_view(), name="delete-question"),
    path("approval/<pk>/", views.question_approval, name="approval"),
    path("faculty-question/<faculty>/",
         views.FacultyQuestionView.as_view(), name="faculty-question"),
    path("dept-question/<dept>/",
         views.DepartmentQuestionView.as_view(), name="dept-question"),
    path("course-question/<course>/",
         views.CourseQuestionView.as_view(), name="course-question"),
    path('question-generate/<pk>/', views.GenerateQuestion.as_view(),
         name='question-generate'),
    path('create-course-access/<id>/', views.GiveCourseAccessToCreateQuestion.as_view(),
         name='create-course-access'),

]
