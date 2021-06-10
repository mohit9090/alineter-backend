from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404

from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
User = get_user_model()

from . models import Customer

from django.views.decorators.csrf import csrf_protect, csrf_exempt

import random


VERIFICATION_ATTEMPT = 0 #keeps the count for number of times user sends a request to resend OTP (max = 3)
MAX_ATTEMPT = 4
HAS_EXECUTED = False


@csrf_protect
def signup(request):
	if request.POST:
		"""
			Most required validation are done in frontend with javascript
		"""
		try:
			email = request.POST.get('user-email').strip()
			password = request.POST.get('user-password').strip()
			first_name = request.POST.get('user-fName').strip()
			last_name = request.POST.get('user-lName').strip()
			mobile = request.POST.get('user-mobileNum').strip()
			street = request.POST.get('user-street-address').strip()
			city = request.POST.get('user-city').strip()
			pin = request.POST.get('user-pincode').strip()
			state = request.POST.get('user-state').strip()
			country = request.POST.get('user-country').strip()
				

			# check if no field is left empty
			if email and first_name and password and last_name and mobile and street and city and pin and state and country:
				email = email if '.com' in email else email + '.com' # if '.com' is missing in email then add it

				# Create User
				try:
					user = User.objects.create_user(email=email, first_name=first_name, password=make_password(password))
				except:
					messages.warning(request, 'It seems account with this email already exists in our database.')
					return redirect('auth:signup')
				else:
					user.last_name = last_name
					user.save()

				# Create User as Customer
				try:
					customer = Customer.objects.get(user=user)
				except Customer.DoesNotExist:
					messages.warning(request, 'User was not created successfully for this Customer')
					return redirect('auth:signup')
				else:
					customer.mobile = mobile
					customer.street_address = street
					customer.city = city
					customer.pin = pin
					customer.state = state
					customer.country = country
					customer.save()

					messages.success(request, 'Account created successfully.')
					return redirect('auth:set_profile_pic')
			else:
				messages.warning(request, 'Some Fields were kept empty')
				return redirect('auth:signup')
		except:
			messages.error(request, 'Sorry Something went wrong. Check if you have filled all the requireed fields, It seems some parameters required were missing. Try again later')
			return redirect('auth:signup')

	return render(request, 'auth_page/signup.html')


def login(request):
	return render(request, 'auth_page/login.html')


def set_profilepic(request):
	return render(request, 'auth_page/set-pic.html')


def run_once(func):
	def wrapper(*args, **kwargs):
		global HAS_EXECUTED
		if not HAS_EXECUTED:
			HAS_EXECUTED = True
			return func(*args, **kwargs)
	HAS_EXECUTED = False
	return wrapper

def if_attempt_left(func):
	def wrapper(request, *args, **kwargs):
		global VERIFICATION_ATTEMPT
		if VERIFICATION_ATTEMPT >= MAX_ATTEMPT:
			return HttpResponse("max limit reached . going to delete the account")
		else:
			return func(request, *args, **kwargs)
	return wrapper

@run_once
def generateOTP(request):
	otp = str(random.randint(11111,99999))
	print(otp)
	request.session['sessionotp'] = make_password(otp)
	# ----------- send mail to user ---------------- #
	return request.session['sessionotp']


@if_attempt_left
def otp_verification(request):
	global VERIFICATION_ATTEMPT
	VERIFICATION_ATTEMPT = VERIFICATION_ATTEMPT+1

	o = generateOTP(request) # will run only once
	
	if request.GET:
		if request.GET.get('r') == 't':
			global HAS_EXECUTED
			HAS_EXECUTED = False
			o = generateOTP(request)

	if request.POST:
		i = request.POST.get('otp')

		try:
			request.session['sessionotp']
		except:
			# ------------ do something here -------------------- #
			print("here")
			pass 
		else:
			if check_password(i, request.session['sessionotp']):
				print("match")
			else:
				print("not match")

			del request.session['sessionotp']

	return render(request, 'auth_page/verify-account.html')