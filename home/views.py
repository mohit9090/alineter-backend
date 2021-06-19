from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from auth_page.models import Customer

from company.models import CompanyReview
# import uuid

User = get_user_model()

def home(request):
	context = {}

	# u = User.objects.get(email=request.user.email)
	# print(u.customer.mobile)

	# print(request.user.customer.mobile)
	# print("img: ",type(request.user.customer.profile_pic))

	# if request.user.customer.profile_pic:
	# 	print("image there")
	# else:
	# 	print("no image there")

	return render(request, 'home/index.html', context)



def company_reviews(request):
	reviews = CompanyReview.objects.all()

	reviewers = [] 

	for rev in reviews: 
		reviewer = {}
		reviewer['name'] = rev.user.get_full_name()
		if rev.user.customer.profile_pic:
			reviewer['img'] = rev.user.customer.profile_pic.url
		else:
			reviewer['img'] = 'https://i.imgur.com/jQWThIn.jpg'
		
		_review = {}
		_review['content'] = rev.review
		_review['rating'] = rev.rating
		
		reviewer['review'] = _review

		reviewers.append(reviewer)


	return JsonResponse(reviewers, safe=False)



# testing purpose
def base(request):
	return render(request, 'home/base.html')






"""


>>> from django.contrib.auth import get_user_model
>>> from django.contrib.auth.models import Group
>>> User = get_user_model()

>>> u1 = User.objects.get(email="mahitkumar166@gmail.com")
>>> u1  --> <User: mahitkumar166@gmail.com>

>>> gall = Group.objects.all()
>>> gall
<QuerySet [<Group: customer>, <Group: employee>, <Group: admin>]>
>>> g1.name  --> 'customer'

>>> u1.groups  --> <django.db.models.fields.related_descriptors.create_forward_many_to_many_manager.<locals>.ManyRelatedManager object at 0x045AC850>

>>> u1.groups.all()  --> <QuerySet [<Group: customer>]>
>>> u1.groups.all()[0].name  --> 'customer'



# SET EXPIRY OF SESSION
if request.GET:
		request.session['fav-lang'] = 'javascript'
		request.session.set_expiry(120)
	print(request.session.get('fav-lang'))


# SET SIMPLE COOKIE
if request.GET:
		# set cookie
		print("setting cookie")
		response = redirect("home:home")
		response.set_cookie('dataflair', 'Hello this is your cookies', max_age = None)
		return response
	try:
		request.COOKIES.get('dataflair')
	except:
		print("no cookies")
	else:
		print(request.COOKIES.get('dataflair'))


# SET COOKIE

import datetime
from django.conf import settings

def set_cookie(response, key, value, days_expire=7):
	if days_expire is None:
		max_age = 365 * 24 * 60 * 60 # one year in seconds
	else:
		max_age = days_expire*24*60*60 # in seconds

	expires = datetime.datetime.strftime(
			datetime.datetime.now() + datetime.timedelta(seconds=max_age),
			"%a, %d-%b-%Y %H:%M:%S"
	)

	response.set_cookie(
		key=key,
		value=value,
		max_age=max_age,
		expires=expires,
		domain=settings.SESSION_COOKIE_DOMAIN,
		secure=settings.SESSION_COOKIE_SECURE or None,
	)

	return response

def home(request):
	if request.GET:
			response = redirect('home:home')
			return set_cookie(response, 'eryu-dsfh-sadj-sdss', [1, 2, 3, 4]) # product_id , product_count

		if request.COOKIES.get('visit') is not None:
			# cookie is already set
			print("cookie is set")
			print("VISIT: ",request.COOKIES.get('eryu-dsfh-sadj-sdss'))
		else:
			# cookie is not set
			print("cookie is not set")

	return render(request, 'home/index.html')

"""