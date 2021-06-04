from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect


def faq(request):
	return render(request, 'company_policy/faq.html')


def cancellation_refund(request):
	return render(request, 'company_policy/cancellation-refund.html')


def terms_condition(request):
	return render(request, 'company_policy/terms.html')


def ordering_terms(request):
	return render(request, 'company_policy/ordering-terms.html')


def redirect_default(request):
	return redirect('policy:faq')
