from django.urls import path
from . import views 

app_name = 'company'

urlpatterns = [
    path('', views.redirect_default, name='redirect_default'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('faq/', views.faq, name='faq'),
    path('feedback/', views.write_about_us, name='write_about_us')
]