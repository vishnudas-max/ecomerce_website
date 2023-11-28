from django.shortcuts import render,HttpResponse,redirect
from user.models import customer
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.
def dashboard(request):
    if 'admin' in request.session:
      return render(request,'admindashboard.html')
    else:
        return redirect(admin_login)

def add_product(request):
    return render(request,'page-form-product-1.html')
  

def product_list(request):
    return render(request,'page-products-list.html')

# ------------------------------------------- VARIENT MANAGEMENT ------------------------------------------

def varient(request):
    return render(request,'varient.html')

# ------------------------------------------BRAND MANAGEMENT ---------------------------------------
from .forms import ImageForm,CategoryForm
from .models import brand,category
def brands(request):
    try:
        b_data=brand.objects.all().order_by('id')
        if request.method == 'POST':
             form = ImageForm(request.POST, request.FILES)
             if form.is_valid():
                form.save()
                return redirect(brands)
        else:
            form = ImageForm()
           
            return render(request, 'page-brands.html',{"form": form,'c':b_data})

    except Exception as e:
        return HttpResponse(e)
    

# ---------------------------------------------------------------------BRAND BLOCKER----------------------------------

def brand_blocker(request,brand_id):
    try:
        current_brand=brand.objects.get(id=brand_id)
        if current_brand.is_active == True:
            brand.objects.filter(id=brand_id).update(is_active='False')
        else:
            brand.objects.filter(id=brand_id).update(is_active='True')
        return redirect(brands)
    except Exception as e:      
        return HttpResponse(e)
   


# -------------------------------------------------------- CATEGORY MANAGEMENT --------------------------------------
def category_(request):
    try:
       c_data=category.objects.all().order_by('id')
       if request.method == 'POST':
           form=CategoryForm(request.POST)
           if form.is_valid():
               form.save()
               return redirect(category_)
       else:
            form=CategoryForm()
       return render(request,'page-categories.html',{"category_form":CategoryForm,"category_data":c_data})
    except Exception as e:
        return HttpResponse(e)
    

# ----------------------------------------------CATEGORY BLOCKER ------------------------------------------------
def category_blocker(request,cat_id):
    try:
        category_item=category.objects.get(id=cat_id)
        if category_item.is_active == True:
            category.objects.filter(id=cat_id).update(is_active='False')
        else:
            category.objects.filter(id=cat_id).update(is_active='True')
        return redirect(category_)
    except Exception as e:      
        return HttpResponse(e)
   

# ----------------------------------------------- ADMMIN LOG OUT-----------------------------------------------------
def admin_logout(request):
    request.session.clear()
    return redirect(admin_login)

# -----------------------------------------     ADMIN LOGIN -------------------------------
def admin_login(request):
    try:
        if request.method == 'POST':
            username=request.POST['username']
            pasword=request.POST['password']
            try:
                user=customer.objects.get(username=username)
            except:
                messages.info(request,'Username or Password does not match !')
                return redirect(admin_login)
            if user.username == username and user.password==pasword:
                request.session['admin']=user.email
                return redirect(dashboard)
            else:
                messages.info(request,'Usernae or Password does not match !')
                return redirect(admin_login)
                

        return render(request,'admin_login.html')
    except Exception as e:
        return HttpResponse(e)
  