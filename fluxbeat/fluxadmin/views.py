from django.shortcuts import render,HttpResponse,redirect
from user.models import customer
from fluxadmin.models import *
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import *
# Create your views here.
def dashboard(request):
    if 'admin' in request.session:
      
      return render(request,'admindashboard.html',)
    else:
        return redirect(admin_login)


# ----------------------------------ADDING PRODUCT -----------------------------------------

def add_product(request):
    try:
       choices=product.HEADPHONE_TYPES
       category_choice=category.objects.all()
       brand_choice=brand.objects.all()
       if request.method ==  'POST':
           product_id=request.POST['product_id']
           product_name=request.POST['product_name']
           product_des=request.POST['product_description']
           product_price=request.POST['product_price']
           product_sale=request.POST['sale_price']
           product_type=request.POST['headphone_type']
           product_cat=request.POST['headphone_cate']
           cate_id=category.objects.get(id=product_cat)
           product_brand=request.POST['headphone_brand']
           brand_id=brand.objects.get(id=product_brand)
           if product.objects.filter(Q(pr_id=product_id) | Q(product_name=product_name)).exists():
               messages.info(request,'Product Already Exists !')
               return redirect(add_product)
           product_obj=product.objects.create(pr_id=product_id,product_name=product_name,description=product_des,product_price=product_price,sale_prce=product_sale,headphone_type=product_type,category_id=cate_id,brand_id=brand_id,total_quantity=0)
           product_obj.save()
       return render(request,'page-form-product-1.html',{'choice':choices,'category_choice':category_choice,'brand_choice':brand_choice})
    except Exception as e:
        return HttpResponse(e)
  



def product_list(request):
    return render(request,'page-products-list.html',)

# ------------------------------------------- VARIENT MANAGEMENT ------------------------------------------

def varient(request):
    try:
   
        product_data=product.objects.all()
        imgag_data=images.objects.all().order_by('-id')
        if request.method == 'POST' and request.FILES.get('varient_color'):
            varient_color=request.FILES.get('varient_color')

            productss=request.POST['product_id']
            productt_id=product.objects.get(id=productss)

            quantity=request.POST['varienet_quantity']
            varient_images = request.POST.getlist('varient_images')

            varient = verients.objects.create(
            varient_color=varient_color,
            quantity=quantity,
            product_id=productt_id
            )

            for image_id in varient_images:
                image = images.objects.get(id=image_id)
                varient.image_field.add(image)
            return redirect(varient)
        else:

            return render(request,'varient_management.html',{'product_data':product_data,'image_data':imgag_data})
    except Exception as e:
        return HttpResponse(e)
    



# ----------------------------------------MULTIPLE IMAGES FOR THE VARIENT -----------------------------------

def varient_img_add(request):
    try:
        if request.method == 'POST' and request.FILES.getlist('varient_images'):
            varient_images=request.FILES.getlist('varient_images')
            owner=request.POST['owner']
            for i in varient_images:
                new_file=images(image_1=i,owner=owner)
                new_file.save()
            return redirect(varient)
        else:
            return redirect(varient)
    except Exception as e:
        return HttpResponse(e)

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
            if user.username == username and user.password==pasword and user.is_superuser:
                request.session['admin']=user.email
                return redirect(dashboard)
            else:
                messages.info(request,'Usernae or Password does not match !')
                return redirect(admin_login)
                

        return render(request,'admin_login.html')
    except Exception as e:
        return HttpResponse(e)
  