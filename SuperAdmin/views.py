from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django import conf
import importlib

def acc_signin(request):
    error_msg = ''
    if request.method == "POST":
        print(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(request.GET.get('next', '/superadmin/'))
        else:
            error_msg = "Invalid username or password"
    return render(request, 'superadmin/signin.html', {'error': error_msg})


def acc_logout(request):
    logout(request)
    return redirect('/')


def admin_index(request):
    for app in conf.settings.INSTALLED_APPS:
        try:
            mod = importlib.import_module('.superadmin', package=app)
            print(mod)
        except ImportError:
            pass
    return render(request, 'superadmin/admin_index.html')

