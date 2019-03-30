from django.contrib import admin
from repository import models


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'email','mobile', 'source', 'consultant', 'status']
    list_filter = ['name', 'company', 'status', 'consultant']


admin.site.register(models.UserProfile)
admin.site.register(models.Role)
admin.site.register(models.Menu)

admin.site.register(models.CustomerInfo, CustomerAdmin)
admin.site.register(models.CustomerFollowUp)
admin.site.register(models.CustomerLevel)
admin.site.register(models.Discount)
admin.site.register(models.DiscountInterval)



admin.site.register(models.Category)
admin.site.register(models.Product)
admin.site.register(models.ProductList)
admin.site.register(models.ProductToImage)
admin.site.register(models.Images)

admin.site.register(models.Cart)
admin.site.register(models.CartToProduct)
admin.site.register(models.Order)

admin.site.register(models.Reply)

