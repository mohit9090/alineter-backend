from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import get_user_model
User = get_user_model()

def after_signup_only(func):
	def wrapper(request, *args, **kwargs):
		try:
			request.session['session_email']
		except:
			# -- Request is not after Signup Page -- #
			return redirect('home:home')
		else:
			return func(request, *args, **kwargs)
	return wrapper

def check_verification(func):
	def wrapper(request, *args, **kwargs):
		signed_user = get_object_or_404(User, email=request.session['session_email'])
		if not signed_user.verified_user:
			""" need for verification """
			return func(request, *args, **kwargs)
		return redirect('home:home')
	return wrapper