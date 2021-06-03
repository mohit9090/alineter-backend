from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect


def signup(request):
	return render(request, 'auth_page/signup.html')


def login(request):
	return render(request, 'auth_page/login.html')


def set_profilepic(request):
	return render(request, 'auth_page/set-pic.html')


def otp_verification(request):
	return render(request, 'auth_page/verify-account.html')