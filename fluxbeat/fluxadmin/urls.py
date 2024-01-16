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
from django.urls import path
from  .import views

urlpatterns = [
    
            path('admin_dashboard',views.dashboard,name='admin_dashboard'),
            path('order_view/<int:order_id>',views.order_view,name='order_view'),
            path('admin_product_page_list',views.product_list,name='product_page_list'),
            path('admin_brand_page',views.brands,name='admin_brand_page'),
            path('admin_add_product',views.add_product,name='admin_add_product'),
            path('admin_product_category',views.category_,name='admin_product_category'),
            path('admin_logout',views.admin_logout,name='admin_logout'),
            path('category_blocker/<int:cat_id>',views.category_blocker,name='category_blocker'),
            path('brand_blocker/<int:brand_id>',views.brand_blocker,name='brand_blocker'),
            path('varient',views.varient,name='varient'),
            path('add_varient_images',views.varient_img_add,name='add_varient_images'),
            path('update_brand/<int:brand_id>',views.update_brand,name='update_brand'),
            path('update_category/<int:category_id>',views.update_category,name='update_category'),
            path('edit_product/<int:product_id>',views.edit_product,name='edit_product'),
            path('product_block/<int:product_id>',views.product_block,name='product_block'),
            path('update_varient/<int:varient_id>',views.update_varient,name='update_varient'),
            path('image_updation/<int:varient_id>',views.image_update,name='image_update'),
            path('user_management',views.user_management,name='user_management'),
            path('user_block/<int:user_id>',views.user_block,name='user_block'),
            path('order_management',views.order_management,name='order_management'),
            path('order_detail/<int:order_id>',views.order_detail,name='order_detail'),
            path('coupon_management',views.coupon_management,name='coupon_mangement'),
            path('edit_coupon/<int:coupon_id>',views.edit_coupon,name='edit_coupon'),
            path('delete_coupon/<int:coupon_id>',views.delete_coupon,name='delete_coupon'),
             path('complete_return/<int:order_id>',views.complete_return,name='complete_return'),
             path('daily_sale',views.daily_sale,name='daily_sale'),
             path('week_sale',views.week_sale,name='week_sale'),
             path('year_sale',views.year_sale,name='year_sale')
        
            
    
]
