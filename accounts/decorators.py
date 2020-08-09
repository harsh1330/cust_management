from django.http import HttpResponse
from django.shortcuts import redirect, render

def authenticared_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_fun):
        def wrapper_fun(request, *args, **kwargs):
            group = None
            
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
                
            if group in allowed_roles:
                return view_fun(request, *args, **kwargs)
            else:
                return render(request, 'accounts/user.html')

        return wrapper_fun
    return decorator