from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect

# Models
from company.models import CompanyTermsCondition, CompanyPrivacyPolicy

# Decorators
from cookie.decorators import check_login_cookie


@check_login_cookie
def cancellation_refund(request):
	return render(request, 'company_policy/cancellation-refund.html')


@check_login_cookie
def terms_condition(request):
	tnc = CompanyTermsCondition.objects.first()
	privacy_policy = CompanyPrivacyPolicy.objects.first()
	context = {'tnc':tnc, 'privacy_policy':privacy_policy}
	return render(request, 'company_policy/terms.html', context)


@check_login_cookie
def ordering_terms(request):
	return render(request, 'company_policy/ordering-terms.html')


@check_login_cookie
def redirect_default(request):
	return redirect('policy:faq')
