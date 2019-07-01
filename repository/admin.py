from django.contrib import admin
from repository import models


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'email','mobile', 'source', 'consultant', 'status']
    list_filter = ['name', 'company', 'status', 'consultant']

class ImageAdmin(admin.ModelAdmin):
    list_display = ['image_tag', 'name']
    fields = ('image_tag', 'name', 'image')
    readonly_fields = ('image_tag',)

admin.site.register(models.UserProfile)
admin.site.register(models.Role)
admin.site.register(models.Menu)
admin.site.register(models.Image, ImageAdmin)

admin.site.register(models.CustomerInfo, CustomerAdmin)
admin.site.register(models.CustomerFollowUp)
admin.site.register(models.CustomerLevel)
admin.site.register(models.Discount)
admin.site.register(models.DiscountInterval)

admin.site.register(models.Category)
admin.site.register(models.Product)

admin.site.register(models.Cart)
admin.site.register(models.CartToProduct)
admin.site.register(models.Order)

admin.site.register(models.Reply)

