from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth.models import User, Group
# from .models import Customer

def signup(request):
	# cust = Customer.objects.get(user=User.objects.last())
	# print(cust.get_address())
	# print(cust.id)
	return render(request, 'auth_page/signup.html')


def login(request):
	return render(request, 'auth_page/login.html')


def set_profilepic(request):
	return render(request, 'auth_page/set-pic.html')


def otp_verification(request):
	return render(request, 'auth_page/verify-account.html')