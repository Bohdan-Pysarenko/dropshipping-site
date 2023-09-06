from .models import *
from django.contrib import admin

# Register your models here.
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Attribute)
admin.site.register(AttributeValue)
admin.site.register(ProductImage)
admin.site.register(ProductAttribute)
admin.site.register(Review)
admin.site.register(ReviewImage)
admin.site.register(Subscription)
admin.site.register(ShippingAddress)
admin.site.register(Coupon)



# @admin.register(ProductAttribute)
# class ProductAttributeAdmin(admin.ModelAdmin):
# 	filter_horizontal = ['attribute', 'value']

