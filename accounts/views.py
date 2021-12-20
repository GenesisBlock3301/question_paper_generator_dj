from django.shortcuts import redirect, render
from . models import User
from django.views import View
from django.contrib import messages
from django.contrib.auth import login as user_login, authenticate
from .forms import ProfileForm
from question_generator.models import Profile, Question


class LoginView(View):
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        user = authenticate(email=email, password=password)
        print(email,password,user)
        if user is not None:
            user_login(request, user)
            if user.is_teacher:
                return redirect("create-profile")
            return redirect('register')
        else:
            return redirect("register")
        return render(request, 'login.html')


class RegistrationView(View):
    def get(self, request):
        context = {
            'name':"User register"
        }
        return render(request, 'register.html',context)

    def post(self, request):
        email = request.POST.get("email", None)
        password = request.POST.get("password", None)
        cpassword = request.POST.get("cpassword", None)
        print(email, password, cpassword)
        if password == cpassword:
            if len(password) < 8:
                messages.error("Password length must be greater than 8 digit")
            else:
                user = User.objects.filter(email=email).exists()
                if not user:
                    user = User.objects.create_user(
                        email=email, password=password)
                    user.is_teacher = True
                    user.store_pass = password
                    user.save()
                    messages.success(request, "Successfully created user!")
                    return redirect("login")
                else:
                    messages.error(request, "User already exists")
                    return redirect("register")
        else:
            messages.error("Password not match!")
        return render(request, 'register.html')


class AdminRegistrationView(View):
    def get(self, request):
        return render(request, 'admin_reg.html')

    def post(self, request):
        email = request.POST.get("email", None)
        password = request.POST.get("password", None)
        cpassword = request.POST.get("cpassword", None)

        if password == cpassword:
            if len(password) < 8:
                messages.error(request,"Password length must be greater than 8 digit")
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
                    return redirect("login")
                else:
                    messages.error(request, "User already exists")
                    return redirect("aregister")
        else:
            messages.error(request,"Password not match!")
            return redirect("aregister")


class CreateTeacherProfile(View):
    form_class = ProfileForm()

    def get(self, request):
        return render(request, 'profile/profile_form.html', {'form': self.form_class})

    def post(self, request):
        faculty = request.POST.get("faculty", None)
        department = request.POST.get("department", None)
        name = request.POST.get("name", None)
        id_no = request.POST.get("id_no", None)

        profile = Profile.objects.create(
            user=request.user,
            faculty=faculty,
            department=department,
            name=name,
            id_no=id_no
        )
        profile.save()
        return redirect('teacher-profile')


class TeacherList(View):
    def get(self, request):
        # s =  User.objects.filter(is_teacher=True)
        # print(s)
        context = {
            'title': "All Teacher",
            'table_header': ["Name", "Faculty", "Department"],
            'item_list': User.objects.filter(is_teacher=True),
        }
        print(context)
        return render(request, 'teachers/Teacher_list.html', context=context)

class TeacherProfile(View):
    def get(self, request):
        approve = Question.objects.filter(user=request.user,approve=True).count()
        all_count = Question.objects.filter(user=request.user).count()
        try:
            rate = (approve*100)/all_count
        except ZeroDivisionError:
            rate = 0

        context = {
            'teacher': Profile.objects.filter(user=request.user).first(),
            'approve_quesion': approve,
            'not_approve':Question.objects.filter(user=request.user,approve=False).count(),
            'success_rate': rate
        }
        return render(request, "profile/Profile.html",context)

    def post(self, request):
        pass


class TeacherProfileShowAdmin(View):
    def get(self, request,pk):

        approve = Question.objects.filter(user__id=pk,approve=True).count()
        all_count = Question.objects.filter(user__id=pk).count()
        context = {
            'teacher': Profile.objects.filter(user__id=pk).first(),
            'approve_quesion': approve,
            'not_approve':Question.objects.filter(user__id=pk,approve=False).count(),
            'success_rate': (approve*100)/all_count
        }
        return render(request, "profile/Profile.html",context)

    def post(self, request):
        pass
