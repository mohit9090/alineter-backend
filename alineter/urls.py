"""alineter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('auth_page.urls')),
    path('blog/', include('blog.urls')),  
    path('company/', include('company.urls')),  
    path('policy/', include('company_policy.urls')),  
    path('', include('home.urls')),  
]


from django.conf.urls.static import static
from django.conf import settings

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# ERR_HANDLER URL
handler400 = 'ERROR_HANDLER.views.err_400'
handler403 = 'ERROR_HANDLER.views.err_403'
handler404 = 'ERROR_HANDLER.views.err_404'
handler500 = 'ERROR_HANDLER.views.err_500'
