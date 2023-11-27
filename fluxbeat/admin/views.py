from django.shortcuts import render,HttpResponse,redirect
from user.models import customer
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
# Create your views here.
def dashboard(request):
    return render(request,'admindashboard.html')
def product_list(request):
    return render(request,'page-products-list.html')
def brand(request):
    return render(request,'page-brands.html')
def add_product(request):
    return render(request,'page-form-product-1.html')
def category(request):
    return render(request,'page-categories.html')

# -----------------------------------------     ADMIN LOGIN -------------------------------
def admin_login(request):
    try:
        if request.method == 'POST':
            username=request.POST['username']
            pasword=request.POST['password']
            user = authenticate(request, username=username, password=pasword)
            if user is not None and user.is_superuser:
                login(request, user)
                return redirect(dashboard)
            else:
                messages.info(request,'Usernae or Password does not match !')
                return redirect(admin_login)
                

        return render(request,'admin_login.html')
    except Exception as e:
        return HttpResponse(e)
  