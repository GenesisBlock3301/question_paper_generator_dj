from django.shortcuts import redirect, render, HttpResponse
from . models import User
from django.views import View
from django.contrib import messages
from django.contrib.auth import login as user_login, authenticate


class LoginView(View):
    def get(self, request):
        return render(request, "login.html")
    
    def post(self,request):
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        user = authenticate(email=email, password=password)
        print(user)
        if user is not None:
            user_login(request,user)
            return redirect('questions')
        return render(request, 'login.html')


class RegistrationView(View):
    def get(self, request):
        return render(request, 'register.html')

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
                    user.is_active = False
                    user.save()
                    messages.success(request, "Successfully created user!")
                    return redirect("login")
                else:
                    messages.error(request, "User already exists")
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
                messages.error("Password length must be greater than 8 digit")
            else:
                user = User.objects.filter(email=email)
                if not user.exists():
                    user = User.objects.create_user(
                        email=email, password=password)
                    user.is_staff = True
                    user.is_superuser = True
                    user.is_active = False
                    user.save()
                    messages.success(request, "Successfully created user!")
                    return redirect("login")
                else:
                    messages.error(request, "User already exists")
        else:
            messages.error("Password not match!")
