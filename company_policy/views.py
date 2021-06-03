from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect


def faq(request):
	return render(request, 'company_policy/faq.html')


def cancellation_refund(request):
	return render(request, 'company_policy/cancellation-refund.html')


def terms_condition(request):
	return render(request, 'company_policy/terms.html')


def ordering_terms(request):
	return render(request, 'company_policy/ordering-terms.html')
