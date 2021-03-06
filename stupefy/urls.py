"""stupefy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from holidays import views
from django.conf.urls import url,include
from django.contrib.auth import views as auth_views

from accounts import views as accounts_views

urlpatterns = [
    url(r'^login/$', auth_views.LoginView.as_view(), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^register/$', accounts_views.register, name='register'),
    
    path('admin/', admin.site.urls),
    path('holidays/',include('holidays.urls')),
    path('api/holidays/',include('holidays.api.urls'),name='holidays-api'),
    path('index/',views.index,name='index'),
    # path('login/',login_view,name='login'),
    # path('register/',register_view,name='register'),
    # path('logout/',logout_view,name='logout'),

    # path('bag/',include('bag.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)