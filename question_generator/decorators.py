from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages


def teacher_required(function):
    def wrapper(request, *args, **kwargs):
        decorated_view_func = login_required(request)
        if not decorated_view_func.user.is_authenticated:
            messages.warning(request, 'Please login first')
            return redirect('tlogin')
        if not request.user.is_teacher:
            return redirect('landing')
        else:
            return function(request, *args, **kwargs)
    return wrapper


def admin_required(function):
    def wrapper(request, *args, **kwargs):
        decorated_view_func = login_required(request)
        if not decorated_view_func.user.is_authenticated:
            messages.warning(request, 'Please login first')
            return redirect('alogin')
        if not request.user.is_staff:
            return redirect('landing')
        else:
            return function(request, *args, **kwargs)
    return wrapper
