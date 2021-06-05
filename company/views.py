from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect


def about(request):
	return render(request, 'company/about.html')


def contact(request):
	return render(request, 'company/contact.html')


def faq(request):
	return render(request, 'company/faq.html')


def write_about_us(request):
	return render(request, 'company/wba.html')


def redirect_default(request):
	return redirect('company:about')