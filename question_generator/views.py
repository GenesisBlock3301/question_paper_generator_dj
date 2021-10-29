from django import forms, views
from django.shortcuts import render
from django.views import View

from question_generator.models import Question
from .forms import CreationQuestionForm


class LandingView(View):
    def get(self, request):
        return render(request, "landing.html")


class FacultyView(View):
    def get(self, request):
        return render(request, 'faculty.html')


class DepartmentView(View):
    def get(self, request):
        return render(request, 'department.html')

class CourseView(View):
    def get(self, request):
        return render(request, 'course.html')

class CreateQuestion(View):
    def get(self,request):
        form = CreationQuestionForm()
        return render(request,"create-question.html",{'form':form})


# AJAX
def load_course(request):
    questions = Question.objects.all()
    return render(request, 'course_dropdown.html', {'questions': questions})