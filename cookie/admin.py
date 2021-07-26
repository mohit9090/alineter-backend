from django.contrib import admin
from . models import Cookie

class CookieAdmin(admin.ModelAdmin):
	readonly_fields = ('user', 'cookie_id', 'creation_date', 'expiry_date') 
	list_display = ['user', 'cookie_id', 'creation_date', 'expiry_date']
	list_filter = ['creation_date', 'expiry_date']
	ordering = ['-creation_date']


admin.site.register(Cookie, CookieAdmin) # in live version it shouldn't be there 
