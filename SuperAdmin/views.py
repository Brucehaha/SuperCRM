from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .utils.paginator import MyPaginator
from SuperAdmin import app_setup
from .forms import dynamic_form_generator
from .utils.image import handelImage
import json
from django.conf import settings


app_setup.superadmin_auto_discover()

from SuperAdmin.sites import site


# def ajaxUpload(request):
#     if request.is_ajax(): # 'X-Requested-With' = 'XMLHttpRequest'
#         root = settings.MEDIA_ROOT
#         key, file = list(request.FILES.items())[0]
#         file_name = file.name
#         file_path = os.path.join(root, str(request.user), 'delete', file_name)
#         if not os.path.exists(os.path.dirname(file_path)):
#             try:
#                 os.makedirs(os.path.dirname(file_path))
#             except OSError as exc:  # Guard against race condition
#                 print('file is not found or not accessible')
#         file_url = os.path.join('media', 'delete', file_name)
#         with open(file_path, 'wb') as f:
#             for line in file.chunks():
#                 f.write(line)
#
#         res = {
#             'file_name': file_name,
#             'data': file_url,
#             'key': key
#         }
#     else:
#         return redirect('/')
#
#     return HttpResponse(json.dumps(res))

def ajaxUpload(request):
    if request.is_ajax():  # 'X-Requested-With' = 'XMLHttpRequest'
        handelImage.register(request, settings.MEDIA_ROOT, settings.MEDIA_URL, 'delete')
        handelImage.create_file()

        res = {
            'file_name': handelImage.get_file_name(),
            'data': handelImage.get_media_url(),
        }
        return HttpResponse(json.dumps(res))
    else:
        return redirect('/')

@login_required
def apps_list(request):
    """ return all the models of each apps """
    return render(request, 'superadmin/apps_list.html', {'site': site})


def app_models_list(request, app_name):
    """ return model list of app """
    models_list = site.enabled_admins[app_name]
    return render(request, 'superadmin/models_list.html', {'models_list': models_list, 'app_name': app_name})


def get_filter_result(request, queryset):
    filter_conditions = {}
    items_dict = request.GET.items()
    for k, v in items_dict:
        if k in ['p', '_o', '_q']:continue
        if v:
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


def get_search_result(request, querysets, admin_class):
    search_key = request.GET.get('_q')
    if search_key:
        q = Q()
        q.connector = 'OR'
        for s in admin_class.search_fields:
            q.children.append(("%s__contains"% s, search_key))
        return querysets.filter(q)
    return querysets


def table_list(request, app_name, model_name):
    ''' return all the instances given model name and app_name'''
    admin_class = site.enabled_admins[app_name][model_name]
    p = request.GET.get('p', 1)
    # get query set
    queryset = admin_class.model.objects.all()
    #filter the queryset
    queryset, filter_conditions = get_filter_result(request, queryset)
    # filter condition will be used in the template tags function which
    # render it to template again for next order or search
    admin_class.filter_conditions = filter_conditions
    # sort the queryset
    queryset, curr_column = get_order_result(request, queryset, admin_class)
    queryset = get_search_result(request, queryset, admin_class)
    # pagenate the pages
    total = admin_class.model.objects.count()
    page = MyPaginator(current_page=int(p), total_items=total, num_per_page=50)
    if queryset.last() is not None:
        queryset = queryset[page.start:page.end]

    return render(request, 'superadmin/table_list.html', {
        'queryset': queryset,
        'admin_class': admin_class,
        'page': page,
        'curr_column': curr_column,
        'app_name': app_name,
        'model_name': model_name})


def add_instance(request, app_name, model_name):
    admin_class = site.enabled_admins[app_name][model_name]
    model_form = dynamic_form_generator(admin_class, form_add=True)
    print(request.FILES)

    if request.method == 'POST':
        form_obj = model_form(request.POST, request.FILES)
        if form_obj.is_valid():
            form_obj.save()
            return redirect("/superadmin/%s/%s/" %(app_name, model_name))
    else:
        form_obj = model_form()
    return render(request, 'superadmin/add.html', locals())


def edit_instance(request, app_name, model_name, obj_id):
    admin_class = site.enabled_admins[app_name][model_name]
    obj = admin_class.model.objects.get(id=obj_id)
    model_form = dynamic_form_generator(admin_class)

    if request.method == 'POST':
        form_obj = model_form(request.POST, request.FILES, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect("/superadmin/%s/%s/" %(app_name, model_name))
    else:
        form_obj = model_form(instance=obj)
    return render(request, 'superadmin/edit.html', locals())


def acc_signin(request):
    error_msg = ''
    if request.method == "POST":
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



