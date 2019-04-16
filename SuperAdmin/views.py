from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from SuperAdmin import app_setup

app_setup.superadmin_auto_discover()

from SuperAdmin.sites import site



@login_required
def app_index(request):
    return render(request, 'superadmin/app_index.html', {'site': site})

def table_filter(request, queryset):
    filter_conditions = {}
    for k, v in request.GET.items():
        if v:
            filter_conditions[k] = v
    return queryset.filter(**filter_conditions), filter_conditions

def table_list(request, app_name, model_name):

    admin_class = site.enabled_admins[app_name][model_name]
    queryset = admin_class.model.objects.all()
    res, filter_conditions = table_filter(request, queryset)
    admin_class.filter_conditions = filter_conditions

    return render(request, 'superadmin/table_list.html', {'queryset': res, 'admin_class': admin_class})


def app_list(request):
    return HttpResponse("app_list")

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



