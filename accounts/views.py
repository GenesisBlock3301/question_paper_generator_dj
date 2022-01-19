from django.forms.models import model_to_dict
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import User
from django.views import View
from django.contrib import messages
from django.contrib.auth import login as user_login, authenticate
from .forms import ProfileForm
from question_generator.models import Profile, Question
from question_generator.decorators import teacher_required, admin_required
from django.contrib.auth import logout
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


def logout_view(request):
    logout(request)
    return redirect("landing")


class TeacherLoginView(View):
    def get(self, request):
        context = {
            'name': "Teacher Login"
        }
        return render(request, "login.html", context)

    def post(self, request):
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        user = authenticate(email=email, password=password)
        print(email, password, user)
        if user is not None:
            user_login(request, user)
            if Profile.objects.filter(user__email=request.user).exists():
                return redirect("pquestions")
            if user.is_teacher:

                return redirect("create-profile")
            if user.is_staff:
                return redirect("teachers")

            return redirect('tlogin')
        else:
            messages.error(request, "Invalid credential")
            return redirect("tlogin")


class AdminLoginView(View):
    # @method_decorator(admin_required)
    def get(self, request):
        context = {
            'name': "Admin login"
        }
        return render(request, "login.html", context)

    def post(self, request):
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        user = authenticate(email=email, password=password)
        print(user)
        if user is not None:
            user_login(request, user)
            return redirect('teachers')
        else:
            messages.error(
                request, "User doesn't exist")
            return redirect("alogin")


class TeacherRegistrationView(View):
    # @method_decorator(admin_required)
    def get(self, request):
        context = {
            'name': "Teacher register"
        }
        return render(request, 'teachers/teacher_register.html', context)

    def post(self, request):
        email = request.POST.get("email", None)
        id_no = request.POST.get("id_no", None)
        password = request.POST.get("password", None)
        cpassword = request.POST.get("cpassword", None)

        if password == cpassword:
            if len(password) < 8:
                messages.error(
                    request, "Password length must be greater than 8 digit")
            else:
                user = User.objects.filter(email=email).exists()
                if not user:
                    user = User.objects.create_user(
                        email=email, password=password, id_no=id_no)
                    user.is_teacher = True
                    user.store_pass = password
                    user.save()
                    messages.success(request, "Successfully created user!")
                    return redirect("teachers")
                else:
                    messages.error(request, "User already exists")
                    return redirect("tregister")
        else:
            messages.error(request, "Password not match!")
        return render(request, 'teachers/teacher_register.html')


class AdminRegistrationView(View):
    def get(self, request):
        context = {
            'name': "Admin register"
        }
        return render(request, 'admins/admin_register.html', context)

    def post(self, request):
        email = request.POST.get("email", None)
        password = request.POST.get("password", None)
        cpassword = request.POST.get("cpassword", None)

        if password == cpassword:
            if len(password) < 8:
                messages.error(
                    request, "Password length must be greater than 8 digit")
                return redirect("aregister")
            else:
                user = User.objects.filter(email=email)
                if not user.exists():
                    user = User.objects.create_user(
                        email=email, password=password)
                    user.is_staff = True
                    user.is_superuser = True
                    user.save()
                    messages.success(request, "Successfully created user!")
                    return redirect("alogin")
                else:
                    messages.error(request, "User already exists")
                    return redirect("aregister")
        else:
            messages.error(request, "Password not match!")
            return redirect("aregister")


class CreateTeacherProfile(View):
    form_class = ProfileForm()

    # @method_decorator(before_create_profile)
    def get(self, request):
        if Profile.objects.filter(user=request.user).exists():
            return redirect("teacher-profile")
        return render(request, 'profile/profile_form.html', {'form': self.form_class, "action": "Create"})

    def post(self, request):
        faculty = request.POST.get("faculty", None)
        department = request.POST.get("department", None)
        name = request.POST.get("name", None)
        image = request.FILES.get("image", None)
        short_name = request.POST.get("short_name", None)

        profile = Profile.objects.create(
            user=request.user,
            faculty=faculty,
            department=department,
            name=name,
            image=image,
            short_name=short_name
        )
        profile.save()
        return redirect('teacher-profile')


class UpdateTeacherProfileView(View):
    form_class = ProfileForm
    template_name = 'profile/profile_form.html'

    def get(self, request, pk):
        instance = get_object_or_404(Profile, id=pk)
        form = self.form_class(model_to_dict(instance=instance))
        return render(request, self.template_name, {'form': form, "action": "Update"})

    def post(self, request, pk):
        instance = get_object_or_404(Profile, id=pk)
        instance.faculty = request.POST.get('faculty', None)
        instance.department = request.POST.get('department', None)
        instance.name = request.POST.get('name', None)
        instance.image = request.FILES.get("image", None)
        instance.short_name = request.POST.get("short_name", None)
        instance.designation = request.POST.get("designation", None)
        instance.save()
        return redirect("teacher-profile")


class TeacherProfile(View):
    @method_decorator(teacher_required)
    def get(self, request):
        approve = Question.objects.filter(
            user=request.user, approve=True).count()
        all_count = Question.objects.filter(user=request.user).count()
        try:
            rate = (approve * 100) / all_count
        except ZeroDivisionError:
            rate = 0

        context = {
            'teacher': Profile.objects.filter(user=request.user).first(),
            'approve_quesion': approve,
            'not_approve': Question.objects.filter(user=request.user, approve=False).count(),
            'success_rate': rate
        }

        return render(request, "profile/Profile.html", context)


class TeacherList(View):
    @method_decorator(admin_required)
    def get(self, request):
        context = {
            'title': "All Teacher",
            'table_header': ["Name", "ID No.", "Short Name", "Faculty", "Department", "Designation", "Action"],
            'item_list': Profile.objects.all(),
        }
        return render(request, 'teachers/Teacher_list.html', context=context)


class TeacherProfileShowAdmin(View):
    def get(self, request, email):
        approve = Question.objects.filter(
            user__email=email, approve=True).count()
        all_count = Question.objects.filter(user__email=email).count()
        context = {
            'teacher': Profile.objects.filter(user__email=email).first(),
            'approve_quesion': approve,
            'not_approve': Question.objects.filter(user__email=email, approve=False).count(),
            'success_rate': (approve * 100) / all_count
        }
        return render(request, "profile/Profile.html", context)


def make_admin(request, id):
    profile = Profile.objects.filter(id=id).first()
    profile.user.is_staff = True if profile.user.is_staff is False else False
    profile.user.save()
    print("user", profile.user.is_staff)
    return redirect("teachers")
