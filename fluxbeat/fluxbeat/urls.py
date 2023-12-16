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
    path('user_logout',views.user_logout,name='user_logout'),
    path('otp',views.send_otp,name='otp'),
    path('otp_varify',views.otp_varify),
    path('flux_admin/',include(urls)),
    path('admin_login',a.admin_login,name='admin_login'),
    path('product_detail/<int:product_id>',views.product_detail,name='product_detail'),
    path('varient_change/<int:product_id>/<int:varient_id>',views.varient_change,name='varient_change'),
    path('user_account',views.user_account,name='user_account'),
    path('user_update/<int:user_id>',views.user_update,name='user_update'),
    path('view_cart',views.view_cart,name='view_cart'),
    path('add_to_cart/<int:product_id>/<int:varient_id>',views.add_to_cart,name='add_to_cart'),
    path('update_quantity/', views.update_quantity, name='update_quantity'),
    path('delete_cart/<int:cart_id>',views.delete_cart,name='delete_cart'),
    path('check_out',views.check_out,name='check_out'),
    path('add_address',views.add_address,name='add_address'),
    path('delete_address/<int:address_id>',views.delete_address,name='delete_address'),
    path('edit_address/<int:address_id>',views.edit_address,name='edit_address'),
    path('cancel_order/<int:order_id>/<str:order_type>',views.cancel_order,name='cancel_order'),
    path('view_order_detailes/<int:order_id>',views.order_detailes,name='order_detailes')

  
    
] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)

