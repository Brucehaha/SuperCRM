from django.conf.urls import url
from SuperAdmin import views


urlpatterns = [
    url(r'^$', views.app_index, name='dashboard'),
    url(r'^signin/', views.acc_signin),
    url(r'^logout/$', views.acc_logout),
    url(r'^(\w+)/(\w+)/(\d+)/edit', views.edit_object, name='edit_object'),
    url(r'^(\w+)/(\w+)', views.table_list, name='table_list'),

]