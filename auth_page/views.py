from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404

from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
User = get_user_model()

from . models import Customer

def signup(request):
	if request.POST:
		try:
			email = request.POST.get('user-email')
			email = email if '.com' in email else email + '.com'
			password = request.POST.get('user-password')
			first_name = request.POST.get('user-fName')
			last_name = request.POST.get('user-lName')
			mobile = request.POST.get('user-mobileNum')
			street = request.POST.get('user-street-address')
			city = request.POST.get('user-city')
			pin = request.POST.get('user-pincode')
			state = request.POST.get('user-state')
			country = request.POST.get('user-country')

			# Create User
			try:
				user = User.objects.create(email=email, first_name=first_name, password=make_password(password))
			except:
				messages.warning(request, 'Account with this email already exists.')
				return redirect('auth:signup')
			else:
				user.last_name = last_name
				user.save()

				# Create User as Customer
				customer = Customer.objects.get(user=user)
				customer.mobile = mobile
				customer.street_address = street
				customer.city = city
				customer.pin = pin
				customer.state = state
				customer.country = country
				customer.save()

				messages.success(request, 'Account created successfully.')
				return redirect('auth:set_profile_pic')
		except:
			messages.error(request, 'Sorry Something went wrong. Try again later')
			return redirect('auth:signup')

	return render(request, 'auth_page/signup.html')


def login(request):
	return render(request, 'auth_page/login.html')


def set_profilepic(request):
	return render(request, 'auth_page/set-pic.html')


def otp_verification(request):
	return render(request, 'auth_page/verify-account.html')




"""

	email = models.EmailField(verbose_name='Email address', max_length=60, unique=True)
	username = models.CharField(verbose_name='Username', max_length=50, blank=True, null=True)
	first_name = models.CharField(verbose_name='First name', max_length=30)
	last_name = models.CharField(verbose_name='Last name', max_length=30)

	# user = models.OneToOneField(User, on_delete=models.CASCADE)
	mobile = models.CharField(verbose_name='Mobile Number', max_length=10)
	# landmark = models.TextField(verbose_name='Landmark', null=True, blank=True)
	street_address = models.TextField(verbose_name='Street Address')
	city = models.CharField(verbose_name='City', max_length=40)
	pin = models.CharField(verbose_name='PIN', max_length=6)
	state = models.CharField(verbose_name='State', max_length=30)
	country = models.CharField(verbose_name='Country', max_length=30)
	# profile_pic = models.ImageField(upload_to=profilepic_directory_path, verbose_name='Profile Pic', blank=True, null=True)

<QueryDict: {
'csrfmiddlewaretoken': ['6LwY3yhmvJHhFRS4R8A68lOtQ4ZoEZu99gPSjHREt0L2iReZsM7qplgi10gtAtGa'], 
'user-fName': ['Mohit'], 
'user-lName': ['Kumar'], 
'user-mobileNum': ['8768757647'], 
'user-email': ['trial100@gmail.com'], 
'user-password': ['Trial100'], 
'confirm-password': ['Trial100'], 
'user-country': ['India'], 
'user-state': ['Odisha'],
'user-city': ['Bhubaneswar'], 
'user-pincode': ['751003'], 
'user-street-address': ['1136/8591 Patitapaban Nagar, Kalpana'], 
'accept-tnc': ['on']}>


2) if email already exists then redirect to signup page with a message
3) if any error them redorect to signup with a message

"""