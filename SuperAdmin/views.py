from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from .utils.paginator import MyPaginator
from SuperAdmin import app_setup

app_setup.superadmin_auto_discover()

from SuperAdmin.sites import site



@login_required
def app_index(request):
    return render(request, 'superadmin/app_index.html', {'site': site})


def table_filter(request, queryset):
    filter_conditions = {}
    items_dict = request.GET.items()
    for k, v in items_dict:
        if k not in ['p', '_o']:
            filter_conditions[k] = v
    return queryset.filter(**filter_conditions), filter_conditions


def table_order_by(request, queryset, admin_class):
    order_id = request.GET.get('_o')
    if not hasattr(admin_class, 'order_by'):
        admin_class.order_by = {}
    if order_id:
        admin_class.order_by['_o'] = order_id
        if order_id.startswith('-'):
            condition = admin_class.list_display[-int(order_id)]
            return queryset.order_by("-%s" % condition)
        else:
            condition = admin_class.list_display[int(order_id)]
            return queryset.order_by(condition)
    else:
        return queryset


def table_list(request, app_name, model_name):
    admin_class = site.enabled_admins[app_name][model_name]
    p = request.GET.get('p', 1)
    total = admin_class.model.objects.count()
    page = MyPaginator(current_page=int(p), total_items=total, num_per_page=50)
    queryset = admin_class.model.objects.all()
    admin_class.filter_conditions = {}
    if queryset.last() is not None:
        queryset, filter_conditions = table_filter(request, queryset)
        queryset = table_order_by(request, queryset, admin_class)
        queryset = queryset[page.start:page.end]
        admin_class.filter_conditions = filter_conditions

    return render(request, 'superadmin/table_list.html', {'queryset': queryset, 'admin_class': admin_class, 'page': page})


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



