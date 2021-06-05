from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect



def store(request):
	return HttpResponse('<h1>Store Page</h1>')