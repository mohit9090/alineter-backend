from django.shortcuts import redirect

def only_unauthenticated_user(view_func):
	def wrapper_unauthenticated_user(request, *args, **kwargs):
		if not request.user.is_authenticated:
			return view_func(request, *args, *kwargs)
		return redirect('home:home')
	return wrapper_unauthenticated_user


def only_authenticated_user(view_func):
	print("decorator B, calling to - ", view_func)
	def wrapper_authenticated_user(request, *args, **kwargs):
		print("wrapper B, calling to - ", view_func)
		if request.user.is_authenticated:
			return view_func(request, *args, **kwargs)
		return redirect('home:home')
	return wrapper_authenticated_user



"""
when session variable is not there but cookie variable is there,
then the pages which allow only unauthenticated user are still allowing authenticated user 
instead if cookie is there then session should be recreated and that passage to the page 
should be blocked

"""
