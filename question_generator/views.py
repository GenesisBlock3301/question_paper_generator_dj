from django import forms, views
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from accounts.models import User
from question_generator.models import Department, Faculty, Profile, Question, Course
from .forms import CreationQuestionForm
from django.views.generic.edit import UpdateView
from django.forms.models import model_to_dict
from django.utils.decorators import method_decorator
from .decorators import teacher_required,admin_required
from django.views.generic.edit import DeleteView
from django.contrib import messages
from django.http import JsonResponse
from .utility import render_to_pdf

class DataTableView(View):
    def get(self, request):
        return render(request, "List_of_item.html")


class LandingView(View):
    def get(self, request):
        if request.user.is_authenticated and request.user.is_teacher:
            return redirect("teacher-profile")
        if request.user.is_staff and request.user.is_authenticated:
            return redirect("teachers")
        return render(request, "landing.html")


class FacultyView(View):
    @method_decorator(admin_required)
    def get(self, request):

        table_header = ['Faculty Name', 'S. Form', 'About Faculty']
        context = {
            'title': "All Faculty",
            'table_header': table_header,
            "item_list": Faculty.objects.all()
        }

        return render(request, 'Faculty/Faculty_list.html', context=context)


class FacultyQuestionView(View):
    @method_decorator(admin_required)
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
        return render(request, 'Faculty/Faculty_question.html', context=context)


class DepartmentView(View):
    @method_decorator(admin_required)
    def get(self, request):

        table_header = ['Dept. Name', 'S. Form', 'About Dept.']
        context = {
            'title': "All Dept",
            'table_header': table_header,
            "item_list": Department.objects.all()
        }

        return render(request, 'Department/Department_list.html', context=context)


class DepartmentQuestionView(View):
    @method_decorator(admin_required)
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
    @method_decorator(admin_required)
    def get(self, request):
        context = {
            'title': "All Courses",
            'table_header': ["Course Title", "About course", "S. Form", "Course Code", "Department"],
            'item_list': Course.objects.all(),
            "course": True
        }
        return render(request, 'Course/Course_list.html', context=context)


class CourseQuestionView(View):
    @method_decorator(admin_required)
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


class CreateQuestion(View):
    # method_decorator()
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
        if request.user.is_teacher:
            return redirect("tpquestions")
        if request.user.is_staff:
            return redirect("questions")


class UpdateQuestionView(View):
    form_class = CreationQuestionForm
    template_name = 'create-question.html'

    def get(self, request, pk):
        instance = get_object_or_404(Question, id=pk)
        form = self.form_class(model_to_dict(instance=instance))
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        instance = get_object_or_404(Question, id=pk)
        # form = self.form_class(request.POST, instance=instance)
        instance.faculty = request.POST['faculty']
        instance.term_name = request.POST['term_name']
        instance.full_mark = request.POST['full_mark']
        instance.difficulty_level = request.POST["difficulty_level"]
        instance.batch = request.POST["batch"]
        instance.department = request.POST["department"]
        instance.course = request.POST["course"]
        instance.duration = request.POST["duration"]
        instance.semester = request.POST["semester"]
        instance.body = request.POST["body"]
        instance.save()
        if request.user.is_teacher:
            return redirect("tpquestions")
        return redirect("pquestions")


class QuestionsView(View):
    @method_decorator(admin_required)
    def get(self, request):
        context = {
            'title': "All Question",
            'table_header': ['Faculty', 'Difficulty Level', 'Department', 'Semester', 'Course', 'Teacher'],
            'item_list': Question.objects.filter(approve=True),
        }
        return render(request, 'Questions/Question_list.html', context=context)


class DeleteQuestionView(DeleteView):
    model = Question
    success_url = "/questions/"


class PendingQuestionView(View):
    @method_decorator(admin_required)
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
        return render(request, 'Admin/AdminPendingQuestion.html', context=context)

@admin_required
def question_approval(request, pk):
    approval = get_object_or_404(Question, id=pk)
    approval.approve = True
    approval.save()
    return redirect("pquestions")

# Teacher portion


class TeacherQuestionView(View):
    @method_decorator(teacher_required)
    def get(self, request):
        context = {
            'title': f"{request.user} Question",
            'table_header': ['Title', 'Difficulty Level', 'Department', 'Semester', 'Course'],
            'item_list': Question.objects.filter(user=request.user, approve=True),
        }

        return render(request, 'Teacher/TeacherQuestion.html', context)


class TeacherPendingQuestionView(View):
    @method_decorator(teacher_required)
    def get(self, request):
        context = {
            'title': f"{request.user} Question",
            'table_header': ['Title', 'Difficulty Level', 'Department', 'Semester', 'Course'],
            'questions': Question.objects.filter(user=request.user, approve=False),
        }
        return render(request, 'Teacher/TeacherPending.html', context=context)


class SingleQuestionView(View):
    def get(self, request, id):
        question = Question.objects.filter(id=id).first()
        return render(request, 'Detail.html', {'question': question, })


class GenerateQuestion(View):
    def get(self, request,pk):
        question = Question.objects.filter(id=pk).first()
        course_code = Course.objects.filter(course_title=question.course).first()
        data = model_to_dict(question)
        data["course_code"] = course_code.course_code
        print(data)
        pdf = render_to_pdf("Questions/Export_Question.html",data)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "question_%s.pdf" %("12341231")
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")


