from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
	path('', views.cart, name='cart'),
	path('fetch-cart/', views.fetch_cart, name='fetch_cart'),
]