from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect


def about(request):
	return render(request, 'company/about.html')


def contact(request):
	return render(request, 'company/contact.html')


def write_about_us(request):
	return render(request, 'company/wba.html')