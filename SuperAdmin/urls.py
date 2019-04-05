from django.conf.urls import url
from SuperAdmin import views

urlpatterns = [
    url(r'^$', views.apps_index, name='dashboard'),
    url(r'^signin/', views.acc_signin),
    url(r'^logout$', views.acc_logout),

]