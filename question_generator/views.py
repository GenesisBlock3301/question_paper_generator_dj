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
        context = {
            'title':"All Departments",
            "sub_title":"Department List"
        }
        return render(request, 'List_of_item.html',context=context)


class DepartmentView(View):
    def get(self, request):
        context = {
            'title':"All Departments",
            "sub_title":"Department List"
        }
        return render(request, 'List_of_item.html',context=context)

class CourseView(View):
   def get(self, request):
        context = {
            'title':"All Courses",
            "sub_title":"Course List"
        }
        return render(request, 'List_of_item.html',context=context)

class CreateQuestion(View):
    def get(self,request):
        form = CreationQuestionForm()
        return render(request,"create-question.html",{'form':form})

class QuestionsView(View):
    def get(self, request):
        context = {
            'title':"All Question",
            "sub_title":"Question List"
        }
        return render(request, 'List_of_item.html',context=context)

# AJAX
def load_course(request):
    questions = Question.objects.all()
    return render(request, 'course_dropdown.html', {'questions': questions})