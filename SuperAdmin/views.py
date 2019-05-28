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


def get_filter_result(request, queryset):
    filter_conditions = {}
    items_dict = request.GET.items()
    for k, v in items_dict:
        print(k, v)
        if k not in ['p', '_o'] and len(v) > 0:
            filter_conditions[k] = v
    return queryset.filter(**filter_conditions), filter_conditions


def get_order_result(request, queryset, admin_class):
    order_id = request.GET.get('_o')
    curr_column = {}
    if order_id:
        condition = admin_class.list_display[abs(int(order_id))]
        curr_column[condition] = order_id
        if order_id.startswith('-'):
            condition= '-'+condition
        return queryset.order_by(condition), curr_column
    return queryset, curr_column


def table_list(request, app_name, model_name):
    admin_class = site.enabled_admins[app_name][model_name]
    p = request.GET.get('p', 1)

    # get query set
    queryset = admin_class.model.objects.all()

    #filter the queryset
    queryset, filter_conditions = get_filter_result(request, queryset)

    # sort the queryset
    queryset, curr_column = get_order_result(request, queryset, admin_class)
    # pagenate the pages
    if queryset.last() is not None:
        total = admin_class.model.objects.count()
        page = MyPaginator(current_page=int(p), total_items=total, num_per_page=50)
        queryset = queryset[page.start:page.end]
        admin_class.filter_conditions = filter_conditions

    return render(request, 'superadmin/table_list.html', {'queryset': queryset, 'admin_class': admin_class, 'page': page, 'curr_column': curr_column})


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



