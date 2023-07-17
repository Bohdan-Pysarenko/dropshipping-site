from .models import *
from django.contrib import admin

# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Attribute)
admin.site.register(AttributeValue)
admin.site.register(Variant)
admin.site.register(ProductImage)
admin.site.register(Review)




@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
	filter_horizontal = ['attribute', 'value']

