from django.shortcuts import redirect

def only_unauthenticated_user(view_func):
	def wrapper_unauthenticated_user(request, *args, **kwargs):
		if not request.user.is_authenticated:
			return view_func(request, *args, *kwargs)
		return redirect('home:home')
	return wrapper_unauthenticated_user


def only_authenticated_user(view_func):
	def wrapper_authenticated_user(request, *args, **kwargs):
		if request.user.is_authenticated:
			return view_func(request, *args, **kwargs)
		return redirect('home:home')
	return wrapper_authenticated_user


