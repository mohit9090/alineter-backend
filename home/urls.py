from django.urls import path
from . import views 

app_name = 'home'

urlpatterns = [
    path('', views.home, name='home'),
    path('company_reviews/', views.company_reviews, name='company_reviews'),
    path('reviews_stats/', views.reviews_stats, name='reviews_stats')
]