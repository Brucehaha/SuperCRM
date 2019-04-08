from repository import models
from SuperAdmin.sites import site
from SuperAdmin.base import  BaseAdminSite

# class Product(models.Model):
#     """Product Table"""
#     name = models.CharField(max_length=64)
#     category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)  # foreign key
#     description = models.TextField(blank=True, null=True)
#     color = models.CharField(max_length=16)
#     width = models.PositiveIntegerField( default=0)
#     thickness = models.PositiveIntegerField(default=0)
#     veneer = models.SmallIntegerField(default=0)
#
#     def __str__(self):
#         return self.name
#
# class ProductList(models.Model):
#     """Product list Table """
#     product = models.ForeignKey("Product", on_delete=models.CASCADE)  # foreign key
#     sku = models.CharField(max_length=16, unique=True)
#     pack_size = models.FloatField()
#     length = models.PositiveSmallIntegerField(default=0)
  #  stock_level = models.FloatField(default=0)


class ProductAdmin(BaseAdminSite):
    list_display = [
        'name',
        'productlist_sku',
        'productlist_length',
        'width',
        'thickness',
        'category',
        'description',
        'productlist_stock_level']



class CustomerAdmin(BaseAdminSite):
    list_display = ['name', 'company', 'email','mobile', 'source', 'consultant', 'status']
    list_filter = ['name', 'company', 'status', 'consultant']


site.register(models.Product, ProductAdmin)
site.register(models.CustomerInfo, CustomerAdmin)
