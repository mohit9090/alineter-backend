from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect

from . models import CompanyReview

from django.contrib import messages


def about(request):
	return render(request, 'company/about.html')


def contact(request):
	return render(request, 'company/contact.html')


def faq(request):
	return render(request, 'company/faq.html')


def write_about_us(request):
	if request.POST:
		""" Get input from the user """
		review = request.POST.get('reviewer-thought')
		rating = int(request.POST.get('reviewer-rating'))
		
		if rating<0 or rating>5:
			messages.warning(request, 'Rating is not in valid range (0-5)')
		else:
			company_review = CompanyReview.objects.create(user=request.user, review=review, rating=rating)
			messages.success(request, 'Thankyou for your honest Review')

	return render(request, 'company/wba.html')


def redirect_default(request):
	return redirect('company:about')

