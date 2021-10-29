from django.shortcuts import render,HttpResponse
from . import models
from django.views import View

def test(request):
    data = "Nayma Islam"
    lis = [1,2,3,4,5,]
    return HttpResponse(f"<div>Hello {data}</div>")


class LoginView(View):
    def get(self,request):
        return render(request,"login.html")

class RegistrationView(View):
    def get(self,request):
        return render(request,'register.html')