from repository import models
from SuperAdmin.sites import site
from SuperAdmin.base import  BaseAdminSite


class ProductAdmin(BaseAdminSite):
    list_display = ['name']



class CustomerAdmin(BaseAdminSite):
    list_display = ['name', 'company', 'email','mobile', 'source', 'consultant', 'status']
    list_filter = ['name', 'company', 'status', 'consultant']


site.register(models.Product, ProductAdmin)
site.register(models.CustomerInfo, CustomerAdmin)
