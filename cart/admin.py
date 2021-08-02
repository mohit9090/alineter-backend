from django.contrib import admin

# Models
from cart.models import TestProduct, TestProductQuantity, ProductCart


# class TestProductAdmin(admin.ModelAdmin):
# 	pass


# class TestProductQuantityAdmin(admin.ModelAdmin):
# 	pass


class ProductCartAdmin(admin.ModelAdmin):
	# readonly_fields = ('date_add', 'date_updated',)
	list_display = ['user', 'product', 'quantity']
	# ordering = ['-date_add']



admin.site.register(TestProduct)
admin.site.register(TestProductQuantity)
admin.site.register(ProductCart, ProductCartAdmin)