from django import forms, views
from django.shortcuts import render
from django.views import View
from question_generator.models import Question
from .forms import CreationQuestionForm


class DataTableView(View):
    def get(self, request):
        return render(request, "List_of_item.html")

class LandingView(View):
    def get(self, request):
        return render(request, "landing.html")


class FacultyView(View):
    def get(self, request):
        table_header = ['Faculty Name','Departments']
        context = {
            'title':"All Departments",
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
             'table_header': ['Title','Difficulty Level','Department','Semester','Course'],
             'questions': Question.objects.filter(approve=True)
        }
        return render(request, 'List_of_item.html',context=context)


# admin monitoring this
class PendingQuestionView(View):
    def get(self, request):
        context = {
            'title':"Pending Question",
             'table_header': ['Title','Difficulty Level','Department','Semester','Course'],
             'questions': Question.objects.filter(approve=False),
             'pending':True
        }
        return render(request, 'List_of_item.html',context=context)


# Teacher portion
class UserQuestionView(View):
    def get(self, request):
        context = {
            'title':f"{request.user} Question",
             'table_header': ['Title','Difficulty Level','Department','Semester','Course'],
             'questions': Question.objects.all(),
             "user_question": True
        }
        return render(request, 'List_of_item.html',context=context)


class SingleQuestionView(View):
    def get(self,request,id):
        question = Question.objects.get(id=id)
        return render(request,'Detail.html',{'question':question,})



# AJAX
def load_course(request):
    questions = Question.objects.all()
    return render(request, 'course_dropdown.html', {'questions': questions})