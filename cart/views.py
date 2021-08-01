from django.shortcuts import render
from django.http import HttpResponse

# Decorators
from accounts.decorators import only_authenticated_user
from cookie.decorators import check_login_cookie


@check_login_cookie
@only_authenticated_user
def cart(request):
	return render(request, 'cart/cart.html')