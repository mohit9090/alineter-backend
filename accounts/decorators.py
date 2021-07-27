from django.shortcuts import redirect
from django.contrib.auth import authenticate, login as login_user, logout as logout_user

from cookie.models import Cookie
from cookie.cookies import set_cookie, delete_cookie

from django.contrib.auth import get_user_model
User = get_user_model()

import datetime
from django.utils import timezone

import pytz

def only_unauthenticated_user(func):
	def wrapper(request, *args, **kwargs):
		if not request.user.is_authenticated:
			return func(request, *args, *kwargs)
		return redirect('home:home')
	return wrapper


def only_authenticated_user(func):
	def wrapper(request, *args, **kwargs):
		cookie_key = 'cookieid'
		response = redirect('home:home')

		# Login Session Exists
		if request.user.is_authenticated:
			return func(request, *args, **kwargs)

		# Cookie Session Exists
		if request.COOKIES.get(cookie_key):
			cookie_id = request.COOKIES.get(cookie_key)
			try:
				user_login_cookie = Cookie.objects.get(cookie_id=cookie_id)
			except Cookie.DoesNotExist:
				# Cookie doesn't exists in database, so delete the cookie from browser
				user_login_cookie = None
				response = delete_cookie(request, response, cookie_key, user=None)
			else:
				# Cookie exists
				if user_login_cookie.expiry_date >= datetime.datetime.now():
					# Recreate login session for the user as cookie hasn't expired
					login_user(request, user_login_cookie.user)

					""" SET SESSION FOR LOGIN """
					SESSION_EXPIRY_AGE = 24*60*60 # 1 day in secs
					request.session.set_expiry(SESSION_EXPIRY_AGE) # expire this session after EXPIRY_AGE		
					return redirect(request.path_info)

				# Delete the cookie as it has been expired
				response = delete_cookie(request, response, cookie_key, user=user_login_cookie.user)

		# No Session Exists
		return response
	return wrapper