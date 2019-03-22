from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """User Info Table"""
    user = models.ForeignKey(User, on_delete=models.CASCADE())
    name = models.CharField(max_length=64)
    email = models.CharField(max_length=64, unique=True)
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
    user = models.OneToOneField(User, null=, blank=True)
    name = models.CharField(max_length=64, default=None)
    company = models.CharField(max_length=64, default=None)
    email = models.CharField(max_length=64, unique=True)
    phone = models.CharField(max_length=64, unique=True)
    mobile = models.CharField(max_length=64, unique=True)
    source_choices = ((0, 'Referral'),
                      (1, 'Web search'),
                      (2, 'Google Ads'),
                      (3, 'Bing Ads'),
                      (4, 'Other'),
                      )
    source = models.SmallIntegerField(choices=source_choices)
    Reference = models.CharField(blank=True, null=True, verbose_name="Refered by")
    consult_product = models.ManyToManyField("Product", verbose_name="Product")
    consult_content = models.TextField()
    status_choices = ((0, 'Unregistered'), (1, "Registered"), (2, "Quited"))
    status = models.SmallIntegerField(choices=status_choices)
    consultant = models.ForeignKey("UserProfile", null=True, black=True, on_delete=models.SET_NULL())
    shipping_address = models.ForeignKey("Address", related_name='shipping', null=True, blank=True, on_delete=models.SET_NULL())
    billing_address = models.ForeignKey("Address", related_name='billing', null=True, blank=True, on_delete=models.SET_NULL())
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class CustomerFollowUp(models.Model):
    """Customer Follow Up"""
    customer = models.ForeignKey("CustomerInfo", on_delete=models.CASCADE())
    content = models.TextField()
    user = models.ForeignKey("UserProfile", "Sales")
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.customer


class Address(models.Model):
    customer = models.ForeignKey("UserProfile", on_delete=models.CASCADE())
    address_type = ((0, 'Billing Address'), (1, "Shipping Address"))
    status = models.SmallIntegerField(choices=address_type)
    street_no = models.CharField(max_length=16)
    street_name = models.CharField(max=64)
    suburb = models.CharField(max=64)
    postcode = models.SmallIntegerField()
    state_choices = (('0', 'VIC'), (1, "NSW"), (2, "QLD"), (3, "SA"), (3, "WA"), (4, 'TAS'))
    status = models.SmallIntegerField(choices=state_choices, default=0)


class Category(models.Model):
    """Category Model"""
    name = models.CharField(max_length=64, unique=True)
    parent = models.ForeignKey("self", on_delete=models.SET_NULL())
    description = models.TextField()

    def __str__(self):
        return self.name


class Product(models.Model):
    """Product Table"""
    name = models.CharField(max_length=64)
    category = models.ForeignKey("Category", on_delete=models.SET_NULL())  # foreign key
    description = models.TextField()
    price = models.PositiveIntegerField()
    color = models.CharField(max_length=16)
    width = models.PositiveIntegerField(max_length=4)
    thickness = models.PositiveIntegerField(max_length=2)
    veneer = models.SmallIntegerField(max_length=1)



class ProductList(models.Model):
    """Product list Table """
    product = models.ForeignKey("Product", on_delete=models.CASCADE())  # foreign key
    sku = models.CharField(max_length=16, unique=True)
    pack_size = models.FloatField(max_length=1)
    length = models.PositiveSMallIntegerField(max_length=4)
    stock_level = models.PositiveSmallIntegerField()

    def __str__(self):
        return "%smm %s"%(self.length, self.product.name)

class Discount(models.Model):
    """Product Discount"""
    product  =


class Images(models.Model):
    name = models.CharField(max_length=64, unique=True)
    product = models.ManyToManyField("Product")  # foreign key
    image = models.ImageField()


class Cart(models.Model):
    """Cart Tabl"""
    user = models.ForeignKey("UserProfile", on_delete=models.CASCADE())
    product = models.ManyToManyField("Product")
    quantity = models.PositiveIntegerField(default=1)


class Order(models.Model):
    """ Order Table"""
    user = models.ForeignKey("UserInfor", null=True, blank=True, on_delete=models.SET_NULL())

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    PAYMENT_METHOD_CHOICES = (
        (0, "Pay on pickup"),
        (1, "Bank Transfer"),
        (2, "Pay over the phone"),
    )
    payment_method = models.PositiveSmallIntegerField(default='0', choices=PAYMENT_METHOD_CHOICES)
    ORDER_STATUS_CHOICES = (
        ('0', 'Proccessing'),
        ('1', 'Paid'),
        ('2', 'Shipped'),
        ('3', 'Picked up'),
    )
    status = models.PositiveSmallIntegerField(default='0', choices=ORDER_STATUS_CHOICES)
    ship_total = models.DecimalField(default=5.99, max_digits=200, decimal_places=2)
    total = models.DecimalField(default=5.99, max_digits=200, decimal_places=2)
    GST = models.DecimalField(default=5.99, max_digits=200, decimal_places=2)
    stub_total = models.DecimalField(default=5.99, max_digits=200, decimal_places=2)

    active = models.BooleanField(default=True)


