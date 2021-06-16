from django.urls import path
from . import views 

app_name = 'auth'

urlpatterns = [
    path('', views.redirect_default, name='redirect_default'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('set-pic/', views.set_profilepic, name='set_profile_pic'),
    path('verify-account/', views.otp_verification, name='otp_verification'),
    path('delete-account/', views.delete_account, name='delete_account')
]