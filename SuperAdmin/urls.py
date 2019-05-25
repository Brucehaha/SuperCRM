from django.conf.urls import url
from SuperAdmin import views


urlpatterns = [
    url(r'^$', views.app_index, name='dashboard'),
    url(r'^signin/', views.acc_signin),
    url(r'^logout/$', views.acc_logout),
    url(r'^(\w+)/(\w+)', views.table_list, name='table_list'),
    # test
    url(r'^order/', views.app_list, name="order_list"),
    url(r'^customer/', views.app_list, name="customer_list"),
    url(r'^signin/', views.app_list, name='product_list'),


]