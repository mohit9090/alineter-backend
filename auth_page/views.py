from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login as login_user, logout as logout_user
from django.contrib import messages
from django.conf import settings
from django.views.decorators.csrf import csrf_protect, csrf_exempt # check
User = get_user_model()

# Models
from auth_page.models import Customer
from cookie.models import Cookie

# Functions
from auth_page.password import generate_password
from cookie.cookies import set_cookie, delete_cookie

# Decorators 
from accounts.decorators import only_unauthenticated_user, only_authenticated_user
from cookie.decorators import check_login_cookie

# Python Import
import random
import datetime


VERIFICATION_ATTEMPT = 0 #keeps the count for number of times user sends a request to resend OTP (max = 3)
MAX_ATTEMPT = 4 # keep it 4
HAS_EXECUTED = False


""" ------------ DECORATORS START ------------- """

def run_once(func):
	def wrapper(*args, **kwargs):
		global HAS_EXECUTED
		if not HAS_EXECUTED:
			HAS_EXECUTED = True
			return func(*args, **kwargs)
	HAS_EXECUTED = False
	return wrapper

def after_signup_only(func):
	def wrapper(request, *args, **kwargs):
		try:
			request.session['session_email']
		except:
			# -- Request is not after Signup Page -- #
			return redirect('home:home')
		else:
			return func(request, *args, **kwargs)
	return wrapper

def check_verification(func):
	def wrapper(request, *args, **kwargs):
		signed_user = get_object_or_404(User, email=request.session['session_email'])
		if not signed_user.verified_user:
			""" need for verification """
			return func(request, *args, **kwargs)
		return redirect('home:home')
	return wrapper

""" ------------ DECORATORS END ------------- """



def redirect_default(request):
	return redirect('auth:login')


@check_login_cookie
@only_unauthenticated_user
def signup(request):
	if request.POST:
		""" Most required validation are done in frontend with javascript """
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
					user = User.objects.create_user(email=email, first_name=first_name, password=password)
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
					# Create session for email ofr other parts of signup section
					request.session['session_email'] = email

					return redirect('auth:otp_verification')
			else:
				messages.warning(request, 'Some Fields were kept empty')
				return redirect('auth:signup')
		except:
			messages.error(request, 'Sorry Something went wrong. Check if you have filled all the requireed fields, It seems some parameters required were missing. Try again later')
			return redirect('auth:signup')

	return render(request, 'auth_page/signup.html')


@check_login_cookie
@only_unauthenticated_user
def login(request):
	if request.POST:
		login_email = request.POST.get('login-email')
		login_password = request.POST.get('login-pwd')
		login_remember = request.POST.get('login-remember-me')

		authenticated_user = authenticate(request, email=login_email, password=login_password)
		if authenticated_user is not None:
			
			if not authenticated_user.verified_user:
				""" Account verification has not been completed for this user """
				messages.warning(request, "It seems that you have not verified your account. First verify it and then try loging in")
				request.session['session_email'] = authenticated_user.email
				return redirect('auth:otp_verification')
			else:
				""" credentials valid and user is also verified so log him in """
				login_user(request, authenticated_user)

				""" SET SESSION FOR LOGIN """
				SESSION_EXPIRY_AGE = 24*60*60 # 1 day in secs
				request.session.set_expiry(SESSION_EXPIRY_AGE) # expire this session after EXPIRY_AGE

				""" SET COOKIES FOR LOGIN (REMEMBER ME) IF ALLOWED"""
				if login_remember:
					# Set Cookie
					COOKIE_EXIPRY_AGE = 60 # 60 days
					response = redirect('home:home')
					cookie_key = 'cookieid'
					cookie_value = generate_password(max_len=32, allow_symbols=False) 
					return set_cookie(request, response, key=cookie_key, value=cookie_value, days_expire=COOKIE_EXIPRY_AGE)

				return redirect('home:home')
		else:
			messages.warning(request, "Credentials are not correct")

	return render(request, 'auth_page/login.html')


@check_login_cookie
@only_authenticated_user
def logout(request):
	cookie_key = 'cookieid'
	response = redirect('home:home')

	""" (REMEMBER ME COOOKIE IS PRESENT), so Delete the Cookie """
	if request.COOKIES.get(cookie_key):
		response = delete_cookie(request, response, cookie_key, user=request.user)

	logout_user(request)
	return response



#----------------------- CHECK DECORATOR


@only_unauthenticated_user
@run_once
def generateOTP(request):
	otp = str(random.randint(11111,99999))
	print(otp)
	request.session['session_otp'] = make_password(otp)
	request.session['trial_otp'] = otp # only for testing purpose
	# ----------- send mail to user ---------------- #
	return request.session['session_otp']



@only_unauthenticated_user
@after_signup_only
@check_verification
def otp_verification(request):
	""" Verification is only required after signup. So this page exists only after signup """
	global VERIFICATION_ATTEMPT

	generated_otp = generateOTP(request) # runs only once

	context = {'verify_email': request.session['session_email']}

	if request.GET:
		if request.GET.get('r') == 't': # GET reuest to re-generate OTP
			global HAS_EXECUTED
			HAS_EXECUTED = False
			generated_otp = generateOTP(request) # request to regenerate OTP

	if request.POST:
		input_otp = request.POST.get('otp')

		try:
			generated_otp = request.session['session_otp']
		except:
			# ------------ do something here otp session is not present-------------------- #
			# This event also occurs when user has entered otp once
			# most probably this case will never arise
			print("here")
			return HttpResponse("Something went wrong")
		else:

			if check_password(input_otp, generated_otp):
				
				signed_user = get_object_or_404(User, email=request.session['session_email'])
				signed_user.verified_user = True
				signed_user.save()				
				
				del request.session['session_otp']
				messages.success(request, 'Account verified successfully.')

				VERIFICATION_ATTEMPT = 0
				return redirect('auth:set_profile_pic')
			else:
				signed_user = get_object_or_404(User, email=request.session['session_email'])
				signed_user.verified_user = False
				signed_user.save()

				context['verification_status'] = 'fail'

	# ORDER OF METHOD IS IMPORTANT
	if VERIFICATION_ATTEMPT >= MAX_ATTEMPT:
		return redirect('auth:delete_account')
	else:
		VERIFICATION_ATTEMPT = VERIFICATION_ATTEMPT + 1

	context['otp'] = request.session['trial_otp'] # only for testing purpose

	return render(request, 'auth_page/verify-account.html', context)



@only_unauthenticated_user
@after_signup_only
def set_profilepic(request):
	session_email = request.session['session_email']

	if request.POST:
		if request.FILES:
			""" File uploaded by user """
			image = request.FILES.get('profile-img')
			signed_user = get_object_or_404(User, email=session_email)
			signed_user.customer.profile_pic = image
			signed_user.save()

		del request.session['session_email']

		messages.info(request, 'Signup Completed. Please Login to continue')
		return redirect('auth:login')

	return render(request, 'auth_page/set-pic.html')



@only_unauthenticated_user
@after_signup_only
def delete_account(request):
	""" Verifcation failed so delete account of the user created just now """
	delete_user = get_object_or_404(User, email=request.session['session_email'])
	delete_user.delete()
	messages.warning(request, 'Account deleted due to successive verification failure or Late response')

	del request.session['session_email']

	global VERIFICATION_ATTEMPT
	VERIFICATION_ATTEMPT = 0

	return redirect('auth:signup')

