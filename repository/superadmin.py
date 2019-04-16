from repository import models
from SuperAdmin.sites import site
from SuperAdmin.base import  BaseAdminSite


class ProductAdmin(BaseAdminSite):
    list_display = [
        'name',
        'productlist__sku',
        'productlist__length',
        'width',
        'veneer',
        'productlist__pack_size',
        'productlist__stock_level',
        'thickness',
        'category',
        ]


class CustomerAdmin(BaseAdminSite):
    list_display = ['name', 'company', 'email', 'mobile', 'source', 'consultant', 'status']
    list_filter = ['name', 'company', 'status', 'consultant', 'timestamp']
    verbose_name = "Customers"


site.register(models.Product, ProductAdmin)
site.register(models.CustomerInfo, CustomerAdmin)
site.register(models.Menu)
