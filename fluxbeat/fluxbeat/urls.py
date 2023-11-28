"""
URL configuration for fluxbeat project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path,include
from user import views
from fluxadmin import urls
from fluxadmin import views as a
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='user_home'),
    path('user_registration',views.user_reg,name='user_reg'),
    path('user_signin',views.user_signin,name='user_signin'),
    path('otp',views.send_otp,name='otp'),
    path('otp_varify',views.otp_varify),
    path('flux_admin/',include(urls)),
    path('admin_login',a.admin_login,name='admin_login')
  
    
] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)

