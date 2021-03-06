"""rulet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.authtoken.views import obtain_auth_token

# Registration
from adminweb import views as account_views 
from django.contrib.auth import views as auth 

urlpatterns = [
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('accounts/', include('django_registration.backends.activation.urls')),
    path('accounts/', include('django.contrib.auth.urls')),

    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),

    # Registration
    path('', include('adminweb.urls')), 
    path('', include('account.urls')), 
    path('login/', account_views.Login, name ='login'), 
    path('logout/', auth.LogoutView.as_view(template_name ='adminweb/login.html'), name ='logout'), 
    path('register/', account_views.register, name ='register'), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
