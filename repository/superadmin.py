from repository import models
from SuperAdmin.sites import site
from SuperAdmin.base import BaseAdminSite


class ProductAdmin(BaseAdminSite):
    list_display = [
        'name',
        'sku',
        'length',
        'width',
        'veneer',
        'pack_size',
        'stock_level',
        'thickness',
        'category',
        ]

    list_filter = ['category']
    search_fields = ['sku', 'name']
    readonly_fields = ['name', 'description']
    image_fields = ['image']
    filter_horizontal = ['category']


class CustomerAdmin(BaseAdminSite):
    list_display = ['name', 'company', 'email', 'mobile', 'source', 'consultant', 'status']
    list_filter = ['consultant', 'timestamp']
    filter_horizontal = ['consult_product']
    verbose_name = "Customers"


class ImageAdmin(BaseAdminSite):
    list_display = ['image_tag', 'name']
    field_order = ['image', 'name']
    image_fields = ['image']
    form_type = 'media'


site.register(models.Product, ProductAdmin)
site.register(models.CustomerInfo, CustomerAdmin)
site.register(models.Menu)
site.register(models.Image, ImageAdmin)
