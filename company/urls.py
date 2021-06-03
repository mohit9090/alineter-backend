from django.urls import path
from . import views 

app_name = 'company'

urlpatterns = [
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('feedback/', views.write_about_us, name='write_about_us')
]