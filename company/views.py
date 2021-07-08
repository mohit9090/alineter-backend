from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from . models import Company, CompanyInfo, CustomerQuery, CompanyReview, CompanyFaq

from django.contrib import messages


def about(request):
	company = Company.objects.first()
	founders = company.companyfounder_set.all()
	context = {'company':company, 'founders':founders}
	return render(request, 'company/about.html', context)


def contact(request):
	company = Company.objects.first()
	company_address = company.companyaddress.get_address()
	company_support_email = company.companyemailhelpline_set.all().get(helpline='support')
	company_telephone = company.companytelephonehelpline_set.all().get(helpline='call')
	context = {
		'address':company_address, 
		'support_email': company_support_email, 
		'telephone': company_telephone
	}
	
	if request.POST:
		company = Company.objects.first()
		print(request.POST)
		customer_name = request.POST.get('mailer-name')
		customer_email = request.POST.get('mailer-email')
		mail_subject = request.POST.get('mail-subject')
		mail_content = request.POST.get('mail-content')
		customer_query = company.customerquery_set.create(name=customer_name, email=customer_email, subject=mail_subject, content=mail_content)

		messages.success(request, 'Thankyou for reaching us.')

	return render(request, 'company/contact.html', context)



def faq(request):
	return render(request, 'company/faq.html')


def fetch_faq(request):
	if request.POST:
		faqs = CompanyFaq.objects.all()
		faqs_arr = []

		for faq in faqs:
			faq_obj = {}
			faq_obj['question'] = faq.question
			faq_obj['answer'] = faq.answer
			
			faqs_arr.append(faq_obj);

		return JsonResponse(faqs_arr, safe=False)
	return HttpResponse("Your are not authorized to access this page.") 

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




