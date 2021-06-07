from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

import uuid


def home(request):
	# print(str(request.user.customer.id) == '94c8bc84-9704-43a4-8a9a-bbd27d4f0f36')
	print(request.user.is_authenticated)
	print(request.user)
	print(request.user.groups)
	return render(request, 'home/index.html')


def base(request):
	return render(request, 'home/base.html')
