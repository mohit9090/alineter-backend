from django.urls import path
from . import views 

app_name = 'auth'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('set-pic/', views.set_profilepic, name='set_profile_pic'),
    path('verify-account/', views.otp_verification, name='otp_verification')
]