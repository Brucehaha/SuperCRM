from repository import models
from SuperAdmin.sites import site


class ProductAdmin(object):
    list_display = ['name']


site.register(models.Product, ProductAdmin)
