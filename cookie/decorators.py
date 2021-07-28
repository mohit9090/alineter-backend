from django.shortcuts import redirect
from django.contrib.auth import login as login_user

# Models
from cookie.models import Cookie
from cookie.cookies import delete_cookie

# Python Import
import datetime


def check_login_cookie(view_func):
	print("decorator A, calling to - ", view_func)
	def wrapper_login_cookie(request, *args, **kwargs):
		cookie_key = 'cookieid'
		print("wrapper A, calling to - ", view_func)

		# Cookie Session Exists
		if not request.user.is_authenticated and request.COOKIES.get(cookie_key):
			cookie_id = request.COOKIES.get(cookie_key)
			try:
				user_login_cookie = Cookie.objects.get(cookie_id=cookie_id)
			except Cookie.DoesNotExist:
				# Cookie doesn't exists in database, so delete the cookie from browser
				user_login_cookie = None
				return delete_cookie(request, view_func(request, *args, **kwargs), cookie_key, user=None)
			else:
				# Cookie exists
				if user_login_cookie.expiry_date >= datetime.datetime.now():
					# Recreate login session for the user as cookie hasn't expired
					login_user(request, user_login_cookie.user)

					""" SET SESSION FOR LOGIN """
					SESSION_EXPIRY_AGE = 24*60*60 # 1 day in secs
					request.session.set_expiry(SESSION_EXPIRY_AGE) # expire this session after EXPIRY_AGE
				else:
					# Delete the cookie as it has been expired
					return delete_cookie(request, view_func(request, *args, **kwargs), cookie_key, user=user_login_cookie.user)
					
		return view_func(request, *args, **kwargs)
	return wrapper_login_cookie