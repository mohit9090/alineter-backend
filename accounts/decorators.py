from django.shortcuts import redirect
from cookie.models import Cookie
import random


def only_unauthenticated_user(func):
	def wrapper(request, *args, **kwargs):
		if not request.user.is_authenticated:
			return func(request, *args, *kwargs)
		return redirect('home:home')
	return wrapper



def only_authenticated_user(func):
	def wrapper(request, *args, **kwargs):
		if request.user.is_authenticated:
			return func(request, *args, **kwargs)
		return redirect('home:home')
	return wrapper