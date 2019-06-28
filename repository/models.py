from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """User Info Table"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    email = models.CharField(max_length=64, unique=True)
    role = models.ManyToManyField("Role")

    def __str__(self): #_unicode__
        return self.name


class Role(models.Model):
    """Role Table"""
    name = models.CharField(max_length=64, unique=True)
    menu = models.ManyToManyField("Menu")

    def __str__(self):
        return self.name


class CustomerInfo(models.Model):

    """Customer Follow Up table"""
    userprofile = models.OneToOneField(UserProfile, related_name="userprofile", null=True, blank=True, on_delete=models.SET_NULL)
    level = models.ForeignKey('CustomerLevel', blank=True, null=True, on_delete=models.CASCADE)
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
    Reference = models.CharField(max_length=20, blank=True, null=True, verbose_name="Refered by")
    consult_product = models.ManyToManyField("Product", verbose_name="Product")
    consult_content = models.TextField()
    status_choices = ((0, 'Unregistered'), (1, "Registered"), (2, "Quited"))
    status = models.SmallIntegerField(choices=status_choices)
    consultant = models.ForeignKey("UserProfile", related_name="consultant", null=True, blank=True, on_delete=models.SET_NULL)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class CustomerFollowUp(models.Model):
    """Customer Follow Up"""
    customer = models.ForeignKey("CustomerInfo", on_delete=models.CASCADE)
    content = models.TextField()
    user = models.ForeignKey("UserProfile", "Sales")
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.customer


class CustomerLevel(models.Model):
    name = models.CharField(max_length=16)
    level = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.name


class Discount(models.Model):

    """Product Discount"""
    level = models.ForeignKey('CustomerLevel', on_delete=models.CASCADE)
    interval = models.ForeignKey('DiscountInterval',  on_delete=models.CASCADE)
    discount = models.IntegerField(default=0)


class DiscountInterval(models.Model):
    min_quantity = models.IntegerField()
    max_quantiy = models.IntegerField()


class Address(models.Model):
    customer = models.ForeignKey("CustomerInfo", on_delete=models.CASCADE)
    ADDRESS_TYPE_CHOICES = ((0, 'Billing Address'), (1, "Shipping Address"))
    address_type = models.SmallIntegerField(choices=ADDRESS_TYPE_CHOICES)
    street_no = models.CharField(max_length=16)
    street_name = models.CharField(max_length=64)
    suburb = models.CharField(max_length=64)
    postcode = models.SmallIntegerField()
    STATE_CHOICES = (('0', 'VIC'), (1, "NSW"), (2, "QLD"), (3, "SA"), (3, "WA"), (4, 'TAS'))
    state = models.SmallIntegerField(choices=STATE_CHOICES, default=0)

    def __str__(self):
        return "%s %s" % (self.customer.name, self.address_type)


class Category(models.Model):
    """Category Model"""
    name = models.CharField(max_length=64, unique=True)
    parent = models.ForeignKey(to="self", blank=True, null=True,  on_delete=models.SET_NULL)
    description = models.TextField()

    def __str__(self):
        return self.name


class Product(models.Model):
    """Product Table"""
    name = models.CharField(max_length=64)
    image = models.ManyToManyField('Image', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)  # foreign key
    description = models.TextField(blank=True, null=True)
    color = models.CharField(max_length=16)
    width = models.PositiveIntegerField( default=0)
    thickness = models.PositiveIntegerField(default=0)
    veneer = models.SmallIntegerField(default=0)
    sku = models.CharField(max_length=16, null=True, blank=True, unique=True)
    pack_size = models.FloatField()
    length = models.PositiveSmallIntegerField(default=0)
    stock_level = models.FloatField(default=0)

    def __str__(self):
        return self.name


class Image(models.Model):
    ''' images storage'''
    name = models.CharField(max_length=64, unique=True)
    image = models.ImageField()
    timestamp = models.DateField(auto_now_add=True)


class Cart(models.Model):
    """Cart Table"""
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)


class CartToProduct(models.Model):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.FloatField(default=0)
    discount = models.IntegerField(default=0)


class Order(models.Model):
    """ Order Table"""
    user = models.ForeignKey("UserProfile", null=True, blank=True, on_delete=models.SET_NULL)

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    DELIVERY_LOCATION_CHOICES = (
        (0, "Pickup in VIC Depot"),
        (1, "Pickup in  NSW Depot"),
        (2, "Delivery to Your Address"),
    )
    delivery_location = models.PositiveSmallIntegerField(default=0, choices=DELIVERY_LOCATION_CHOICES)
    shipping_address = models.ForeignKey('Address', related_name="shipping", null=True, blank=True, on_delete=models.CASCADE)
    billing_address = models.ForeignKey('Address', related_name="billing", null=True, blank=True, on_delete=models.CASCADE)
    PAYMENT_METHOD_CHOICES = (
        (0, "Pay on pickup"),
        (1, "Bank Transfer"),
        (2, "Pay over the phone"),
    )
    payment_method = models.PositiveSmallIntegerField(default=0, choices=PAYMENT_METHOD_CHOICES)
    ORDER_STATUS_CHOICES = (
        (0, 'Proccessing'),
        (1, 'Paid'),
        (2, 'Shipped'),
        (3, 'Picked up'),
    )
    status = models.PositiveSmallIntegerField(default=0, choices=ORDER_STATUS_CHOICES)
    ship_total = models.DecimalField(default="", max_digits=200, decimal_places=2)
    total = models.DecimalField(default=5.99, max_digits=200, decimal_places=2)
    GST = models.DecimalField(default=5.99, max_digits=200, decimal_places=2)
    stub_total = models.DecimalField(default=5.99, max_digits=200, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.id


class Ticket(models.Model):

    """Customer question ticket"""
    claimer = models.ForeignKey(UserProfile, related_name="claimer", on_delete=models.CASCADE)
    subject = models.CharField(max_length=32)
    timestamp = models.DateTimeField(auto_now_add=True)
    processor = models.ForeignKey(UserProfile,  related_name="processor", blank=True, null=True, on_delete=models.SET_NULL)
    status_choices = [
        (0, 'open'),
        (1, 'processing'),
        (2, 'closed'),

    ]
    status = models.IntegerField(choices=status_choices, default=0)

    def __str__(self):
        return str(self.subject)


class Reply(models.Model):
    content = models.TextField()
    ticket = models.ForeignKey(Ticket,  on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile,  on_delete=models.CASCADE)
    replyTo = models.ForeignKey(to='self',  on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return "%s-%s" %(self.user, self.ticket)


class Menu(models.Model):

    """dynamic menu"""
    name = models.CharField(max_length=64)

    URL_TYPE_CHOICES = ((0, 'absolute'), (1, 'dynamic'))
    url_type = models.SmallIntegerField(choices=URL_TYPE_CHOICES, default=0)
    url_name = models.CharField(max_length=128)
    icon = models.TextField()
    order = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'url_name')
