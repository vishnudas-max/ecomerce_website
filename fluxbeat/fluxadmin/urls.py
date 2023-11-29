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
            path('admin_product_page_list',views.product_list,name='product_page_list'),
            path('admin_brand_page',views.brands,name='admin_brand_page'),
            path('admin_add_product',views.add_product,name='admin_add_product'),
            path('admin_product_category',views.category_,name='admin_product_category'),
            path('admin_logout',views.admin_logout,name='admin_logout'),
            path('category_blocker/<int:cat_id>',views.category_blocker,name='category_blocker'),
            path('brand_blocker/<int:brand_id>',views.brand_blocker,name='brand_blocker'),
            path('varient',views.varient,name='varient'),
            path('add_varient_images',views.varient_img_add,name='add_varient_images')
        
            
    
]
