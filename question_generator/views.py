from django import forms, views
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from question_generator.models import Department, Faculty, Question, Course
from .forms import CreationQuestionForm
from django.views.generic.edit import UpdateView
from django.forms.models import model_to_dict
from django.utils.decorators import method_decorator
from .decorators import teacher_required
from django.views.generic.edit import DeleteView
from django.contrib import messages
from django.http import JsonResponse


class DataTableView(View):
    def get(self, request):
        return render(request, "List_of_item.html")


class LandingView(View):
    def get(self, request):
        return render(request, "landing.html")


class FacultyView(View):
    def get(self, request):

        table_header = ['Faculty Name', 'S. Form', 'About Faculty']
        context = {
            'title': "All Faculty",
            'table_header': table_header,
            "item_list": Faculty.objects.all()
        }

        return render(request, 'Faculty/Faculty_list.html', context=context)


class FacultyQuestionView(View):
    def get(self, request, faculty):
        admin = False
        if request.user.is_staff:
            admin = True
        context = {
            'title': "All Question",
            'table_header': ['Faculty', 'Difficulty Level', 'Department', 'Semester', 'Course'],
            'item_list': Question.objects.filter(approve=True, faculty=faculty),
            'admin': admin,
            "question": True
        }
        return render(request, 'List_of_item.html', context=context)


class DepartmentView(View):
    def get(self, request):

        table_header = ['Dept. Name', 'S. Form', 'About Dept.']
        context = {
            'title': "All Dept",
            'table_header': table_header,
            "item_list": Department.objects.all()
        }

        return render(request, 'Department/Department_list.html', context=context)


class DepartmentQuestionView(View):
    def get(self, request, dept):
        admin = False
        if request.user.is_staff:
            admin = True
        context = {
            'title': "All Question",
            'table_header': ['Faculty', 'Difficulty Level', 'Department', 'Semester', 'Course'],
            'item_list': Question.objects.filter(approve=True, department=dept),
            'admin': admin,
            "question": True
        }
        return render(request, 'Department/Department_Question.html', context=context)


class CoursesView(View):
    def get(self, request):
        context = {
            'title': "All Courses",
            'table_header': ["Course Title", "About course", "S. Form", "Course Code", "Department"],
            'item_list': Course.objects.all(),
            "course": True
        }
        return render(request, 'Course/Course_list.html', context=context)


class CourseQuestionView(View):
    def get(self, request, course):
        admin = False
        if request.user.is_staff:
            admin = True
        context = {
            'title': "All Question",
            'table_header': ['Faculty', 'Difficulty Level', 'Department', 'Semester', 'Course'],
            'item_list': Question.objects.filter(approve=True, course=course),
            'admin': admin,
            "question": True
        }
        return render(request, 'Course/Course_Question.html', context=context)


# @method_decorator(teacher_required)
class CreateQuestion(View):
    def get(self, request):
        form = CreationQuestionForm()
        return render(request, "create-question.html", {'form': form})

    def post(self, request):
        faculty = request.POST.get("faculty", None)
        term_name = request.POST.get("term_name", None)
        full_mark = request.POST.get("full_mark", None)
        difficulty_level = request.POST.get("difficulty_level", None)
        batch = request.POST.get("batch", None)
        department = request.POST.get("department", None)
        duration = request.POST.get("duration", None)
        semester = request.POST.get("semester", None)
        body = request.POST.get("body", None)
        course = request.POST.get("course", None)

        question = Question.objects.create(
            user=request.user,
            faculty=faculty,
            term_name=term_name,
            full_mark=full_mark,
            difficulty_level=difficulty_level,
            batch=batch,
            department=department,
            duration=duration,
            semester=semester,
            body=body,
            course=course
        )
        question.save()
        return redirect('pquestions')


class UpdateQuestionView(View):
    form_class = CreationQuestionForm
    template_name = 'create-question.html'

    def get(self, request, pk):
        instance = get_object_or_404(Question, id=pk)
        form = self.form_class(model_to_dict(instance=instance))
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        instance = get_object_or_404(Question, id=pk)
        form = self.form_class(request.POST, instance=instance)
        instance.faculty = form.data['faculty']
        instance.term_name = form.data['term_name']
        instance.full_mark = form.data['full_mark']
        instance.difficulty_level = form.data["difficulty_level"]
        instance.batch = form.data["batch"]
        instance.department = form.data["department"]
        instance.course = form.data["course"]
        instance.duration = form.data["duration"]
        instance.semester = form.data["semester"]
        instance.body = form.data["body"]
        instance.save()
        return redirect("pquestions")


class QuestionsView(View):
    def get(self, request):
        admin = False
        if request.user.is_staff:
            admin = True
        context = {
            'title': "All Question",
            'table_header': ['Faculty', 'Difficulty Level', 'Department', 'Semester', 'Course', 'Teacher'],
            'item_list': Question.objects.filter(approve=True),
            'admin': admin,
            "question": True
        }
        return render(request, 'Questions/Question_list.html', context=context)


class DeleteQuestionView(DeleteView):
    model = Question
    success_url = "/questions/"


class PendingQuestionView(View):
    def get(self, request):
        admin = False
        if request.user.is_staff:
            admin = True
        item_list = Question.objects.filter(
            approve=False, user=request.user)\
                 if request.user.is_teacher else Question.objects.filter(approve=False)
        context = {
            'title': "Pending Question",
            'table_header': ['Faculty', 'Difficulty Level', 'Department', 'Semester', 'Course'],
            'item_list': item_list

        }
        return render(request, 'List_of_item.html', context=context)


def question_approval(request, pk):
    approval = get_object_or_404(Question, id=pk)
    approval.approve = True
    approval.save()
    return redirect("pquestions")

# Teacher portion


class UserQuestionView(View):
    def get(self, request):
        context = {
            'title': f"{request.user} Question",
            'table_header': ['Title', 'Difficulty Level', 'Department', 'Semester', 'Course'],
            'questions': Question.objects.all(),
            "user_question": True
        }
        return render(request, 'List_of_item.html', context=context)


class SingleQuestionView(View):
    def get(self, request, id):
        question = Question.objects.filter(id=id).first()
        return render(request, 'Detail.html', {'question': question, })


# AJAX


def load_course(request):
    questions = Question.objects.all()
    return render(request, 'course_dropdown.html', {'questions': questions})
