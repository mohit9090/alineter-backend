from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect


def home(request):
	return render(request, 'home/index.html')


def base(request):
	return render(request, 'home/base.html')
