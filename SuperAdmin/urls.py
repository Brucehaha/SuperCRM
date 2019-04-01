from django.conf.urls import url
from SuperAdmin import views

urlpatterns = [
    url(r'^$', views.admin_index),
    url(r'^signin/', views.acc_signin),
    url(r'^logout$', views.acc_logout),

]