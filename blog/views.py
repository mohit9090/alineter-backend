from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

# Decorators
from cookie.decorators import check_login_cookie


@check_login_cookie
def blog(request):
	return render(request, 'blog/blog.html') 