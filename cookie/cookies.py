from django.conf import settings
# Models
from cookie.models import Cookie
# Python Import
import datetime

""" ------------ SET COOKIE FUNCTION -------- """
def set_cookie(request, response, key, value, days_expire=7):
	if not key or not value or not request.user:
		return response
	
	cookie_max_age = days_expire * 24 * 60 * 60 # days_expire in seconds
	cookie_expiry_date = datetime.datetime.now() + datetime.timedelta(seconds=cookie_max_age)
	format_expiry_date = datetime.datetime.strftime(cookie_expiry_date, "%a, %d-%b-%Y %H:%M:%S")
	response.set_cookie(
		key=key,
		value=value,
		expires=format_expiry_date,
		domain=settings.SESSION_COOKIE_DOMAIN,
		secure=settings.SESSION_COOKIE_SECURE or None,
	)
	# Create Cookie model for current user instance
	cookie = Cookie.objects.create(
		user=request.user, 
		cookie_id=value, 
		expiry_date=cookie_expiry_date
	)
	return response


""" ----------- DELETE COOKIE FUNCTION ---------- """
def delete_cookie(request, response, key, user):
	response.delete_cookie(key)
	# Delete Cookie from model for current user instance
	if user:
		try:
			user_cookie = Cookie.objects.get(user=user)
		except Cookie.DoesNotExist:
			return response
		else:
			user_cookie.delete()
	return response




"""

https://stackoverflow.com/questions/15100400/django-remember-me-with-built-in-login-view-and-authentication-form
https://stackoverflow.com/questions/4609845/in-django-how-is-request-session-set-expiry-used-to-log-out-users-after-idle
https://stackoverflow.com/questions/3529695/how-do-i-set-httponly-cookie-in-django

"""