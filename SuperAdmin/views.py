from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from SuperAdmin import app_setup

app_setup.superadmin_auto_discover()

from SuperAdmin.sites import site


def apps_index(request):
    print("registerd:", site.enabled_admins)
    return render(request, 'superadmin/apps_index.html', {'site': site})

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



