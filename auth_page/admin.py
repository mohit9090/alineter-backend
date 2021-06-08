from django.contrib import admin

from . models import Customer


class CustomerAdmin(admin.ModelAdmin):
	readonly_fields = ('user',) 

	list_display = ['user', 'city', 'pin', 'state']
	list_filter = ['city', 'state', 'pin']
	
	fieldsets = (
		(None, {'fields': ('user', 'mobile',)}),
		('Address', {'fields': ('landmark', 'street_address', 'city', 'pin', 'state', 'country',)}),
		('Profile Pic', {'fields': ('profile_pic',)})
	)

	search_fields = ['user', 'city', 'pin', 'state']
	ordering = ['user']


admin.site.register(Customer, CustomerAdmin)