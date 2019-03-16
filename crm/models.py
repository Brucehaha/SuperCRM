from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """User Info Table"""
    user = models.ForeignKey(User, on_delete=models.CASCADE())
    name = models.CharField(max_length=64)
    role = models.ManyToManyField("Role", blank=True, null=True)

    def __str__(self): #_unicode__
        return self.name


class Role(models.Model):
    """Role Table"""
    name = models.CharField(max_length=64, unique=True)
    def __str__(self):
        return self.name


class CustomerInfo(models.Model):
    """Customer Follow Up table"""
    user = models.ForeignKey(User, on_delete=models.CASCADE())
    name = models.CharField(max_length=64, default=None)
    email = models.CharField(max_length=64, unique=True)
    phone = models.CharField(max_length=64, unique=True)
    mobile = models.CharField(max_length=64, unique=True)
    consult_product = models.ManyToManyField("Product", verbose_name="Product")
    status_choices = ((0, 'Unregistered'), (1, "Registered"), (2, "Quited") )
    consultant = models.ForeignKey("UserProfile", null=True, black=True, on_delete=models.SET_NULL())
    date = models.DateField(auto_now_add=True)


class Category(models.Model):
    "Category Model"


class Product(models.Model):
    """Product Table"""
    pass


class ProductList(models.Model):
    """Product list Table """
    pass


class Cart(models.Model):
    """Cart Table===course reacord"""
    pass


class Order(models.Model):
     """ Order Table"""

