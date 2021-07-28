from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect

# Decorators
from cookie.decorators import check_login_cookie


@check_login_cookie
def store(request):
	return HttpResponse('<h1>Store Page</h1>')