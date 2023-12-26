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
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='user_home'),
    path('shop_product_list',views.shop_product_list,name='shop_product_list'),
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
    path('update_cart_quantity/<int:cart_item_id>/<str:operation>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('delete_cart/<int:cart_id>',views.delete_cart,name='delete_cart'),
    path('check_out',views.check_out,name='check_out'),
    path('add_address',views.add_address,name='add_address'),
    path('delete_address/<int:address_id>',views.delete_address,name='delete_address'),
    path('edit_address/<int:address_id>',views.edit_address,name='edit_address'),
    path('cancel_order/<int:order_id>/<str:order_type>',views.cancel_order,name='cancel_order'),
    path('view_order_detailes/<int:order_id>',views.order_detailes,name='order_detailes'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('success/<int:order_id>',views.success,name='success')


  
    
] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)

