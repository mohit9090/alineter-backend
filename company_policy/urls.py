from django.urls import path
from . import views 

app_name = 'policy'

urlpatterns = [
    path('', views.redirect_default, name='redirect_default'),
    path('faq/', views.faq, name='faq'),
    path('cancellation-refund/', views.cancellation_refund, name='cancellation_refund'),
    path('terms-condition/', views.terms_condition, name='terms_condition'),
    path('ordering-terms/', views.ordering_terms, name='ordering_terms')
]