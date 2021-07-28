from django.shortcuts import render
# from django.shortcuts import render, redirect, get_object_or_404
# from django.http import HttpResponse, HttpResponseRedirect, Http404
# from django.contrib.auth.models import Group
# from django.contrib.auth import get_user_model
# User = get_user_model()

# Decorator
from accounts.decorators import only_authenticated_user
from cookie.decorators import check_login_cookie


@check_login_cookie 
@only_authenticated_user 
def account(request):
	return render(request, "accounts/account.html")

