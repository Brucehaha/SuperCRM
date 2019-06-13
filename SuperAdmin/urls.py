from django.conf.urls import url
from SuperAdmin import views


urlpatterns = [
    url(r'^$', views.apps_list, name='dashboard'),
    url(r'^(\w+)/$', views.app_models_list, name='models_list'),

    url(r'^(\w+)/(\w+)/(\d+)/edit/$', views.edit_instance, name='edit_instance'),
    url(r'^(\w+)/(\w+)/add/$', views.add_instance, name='add_instance'),

    url(r'^(\w+)/(\w+)/$', views.table_list, name='table_list'),

    url(r'^signin/', views.acc_signin),
    url(r'^logout/$', views.acc_logout),

]