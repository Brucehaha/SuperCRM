from django.conf.urls import url, re_path
from SuperAdmin import views


urlpatterns = [
    re_path(r'^$', views.apps_list, name='dashboard'),
    re_path(r'^signin/', views.acc_signin),
    re_path(r'^logout/$', views.acc_logout),
    re_path(r'^ajax-upload.html/$', views.ajaxUpload),
    re_path(r'^media-gallery.html/$', views.imageListView),

    re_path(r'^(\w+)/$', views.app_models_list, name='models_list'),

    re_path(r'^(\w+)/(\w+)/(\d+)/edit/$', views.edit_instance, name='edit_instance'),
    re_path(r'^(\w+)/(\w+)/add/$', views.add_instance, name='add_instance'),
    re_path(r'^(\w+)/(\w+)/(\d+)/delete/$', views.delete_instance, name='delete_instance'),
    re_path(r'^(\w+)/(\w+)/$', views.table_list, name='table_list'),

]