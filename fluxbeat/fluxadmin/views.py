from django.shortcuts import render,HttpResponse,redirect
from user.models import customer
from fluxadmin.models import *
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import *
import time
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
           product_image=request.FILES.get('product_image')
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
           
           if int(product_price) < int(product_sale):
               messages.info(request,'Sale price must be lower than product price !')
               return redirect(add_product)
           if int(product_price) <=0 and int(product_sale) <=0:
               messages.info(login_required,'Price should Greater than 0 !')
               return redirect(add_product)

           if product.objects.filter(Q(pr_id=product_id) | Q(product_name=product_name)).exists():
               messages.info(request,'Product Already Exists !')
               return redirect(add_product)
           try:
               with Image.open(product_image) as img:
                   width, height = img.size
           except Exception as e:
               messages.info(request,"File type does not match.try to upload image only!")
               return redirect(add_product)
           product_obj=product.objects.create(pr_id=product_id,product_image=product_image,product_name=product_name,description=product_des,product_price=product_price,sale_prce=product_sale,headphone_type=product_type,category_id=cate_id,brand_id=brand_id,total_quantity=0)
           product_obj.save()
           success_message = "Product addes succesfully!"
           return render(request,'page-form-product-1.html',{'choice':choices,'category_choice':category_choice,'brand_choice':brand_choice,'success_message': success_message})
       success_message=False
       return render(request,'page-form-product-1.html',{'choice':choices,'category_choice':category_choice,'brand_choice':brand_choice,'success_message': success_message})
    except Exception as e:
        return HttpResponse(e)
  

# -----------------------------------------------------EDIT PRODUCT---------------------------------------------

def edit_product(request,product_id):
    try:
        j=product.objects.get(id=product_id)
        product_cates=j.product_varients.all()
        choices=product.HEADPHONE_TYPES
        categor=category.objects.all()
        bran=brand.objects.all()
        pro=product.objects.select_related('category_id','brand_id').get(id=product_id)
        if request.method == 'POST':
            product_image=request.FILES.get('product_image')
            product_name=request.POST['product_name']
            product_des=request.POST['product_description']
            prodct_price=request.POST['product_price']
            sale_price=request.POST['sale_price']
            prodcut_type=request.POST['headphone_type']
            h_category=request.POST['headphone_cate']
            h_cate=category.objects.get(id=h_category)
            h_brand=request.POST['headphone_brand']
            h_bran=brand.objects.get(id=h_brand)
            if product.objects.filter(product_name=product_name).exclude(id=product_id).exists():
                messages.info(request,'Product with this name already excists!')
                return render(request,'product_edit.html',{"category_choice":categor,"brand_choice":bran,"pro":pro,"choice":choices,"product_cates":product_cates})
            
            elif int(prodct_price) < int(sale_price):
                messages.info(request,'sale price should be less than product price !')
                return render(request,'product_edit.html',{"category_choice":categor,"brand_choice":bran,"pro":pro,"choice":choices,"product_cates":product_cates})
            
            elif int(prodct_price) < 1 and int(sale_price) < 1:
                messages.info(request,'Price should be greater than zero!')
                return render(request,'product_edit.html',{"category_choice":categor,"brand_choice":bran,"pro":pro,"choice":choices,"product_cates":product_cates})
            
            print(product_image,product_name,product_des,prodct_price,sale_price,prodcut_type,h_category,h_brand)
            p=product.objects.get(id=product_id)
            p.product_name=product_name
            p.description=product_des
            p.product_price=prodct_price
            p.sale_prce=sale_price
            p.headphone_type=prodcut_type
            p.category_id=h_cate
            p.brand_id=h_bran
            if p.product_image:
                p.product_image.delete()
            p.product_image=product_image
            p.save()
            success_message = "Product Updation succes"
            return render(request,'product_edit.html',{"category_choice":categor,"brand_choice":bran,"pro":pro,"choice":choices,"product_cates":product_cates,'success_message': success_message})
        else:
            success_message = False
            return render(request,'product_edit.html',{"category_choice":categor,"brand_choice":bran,"pro":pro,"choice":choices,"product_cates":product_cates,'success_message': success_message})
        
    except Exception as e:
        return HttpResponse(e)

# ----------------------------------------------------------BLOCK PRODUCT ----------------------------------------

def product_block(request,product_id):
    try:
       c=product.objects.get(id=product_id)
       if c.is_active:
           c.is_active ='False'
           c.save()
       else:
           c.is_active ='True'
           c.save()

       return redirect(product_list)
    except Exception as e:
        return HttpResponse(e)


# ---------------------------------------------------------------PRODUCT LISTING -----------------------------------------

def product_list(request):
    try:
        verient=verients.objects.all().order_by('id')
        products = product.objects.select_related('category_id', 'brand_id').all()
        return render(request,'page-products-list.html',{'products':products,"verient":verient})
    except Exception as e:
        return HttpResponse(e)


# ------------------------------------------- VARIENT MANAGEMENT ------------------------------------------

def varient(request):
    try:
   
        product_data=product.objects.all()
        imgag_data=images.objects.all().order_by('-id')
        if request.method == 'POST' and request.FILES.get('varient_color'):
            varient_id=request.POST['varient_id']
            varient_color=request.FILES.get('varient_color')
            productss=request.POST['product_id']
            productt_id=product.objects.get(id=productss)

            vari_id=f"{productt_id.pr_id}-{varient_id}"

            quantity=request.POST['varienet_quantity']
            varient_images = request.POST.getlist('varient_images')
            
            if verients.objects.filter(varient_id=vari_id).exists():
                messages.info(request,'Varient already excits !')
                return redirect(varient)
            
            varien = verients.objects.create(
            varient_id=vari_id,
            varient_color=varient_color,
            quantity=quantity,
            product_id=productt_id
            )

            for image_id in varient_images:
                image = images.objects.get(id=image_id)
                varien.image_field.add(image)

            prod_qunt=product.objects.get(id=productss)
            prod_qunt.total_quantity += int(quantity)
            prod_qunt.save()

            
            return redirect(varient)
        else:

            return render(request,'varient_management.html',{'product_data':product_data,'image_data':imgag_data})
    except Exception as e:
        return HttpResponse(e)
    

# ----------------------------------------   UPDATE VARIENT --------------------------------------------
def update_varient(request,varient_id):
    try:
        img=images.objects.all().order_by('-id')
        varient=verients.objects.select_related('product_id').get(id=varient_id)

        if request.method == 'POST':
            
            varient_color=request.POST['varient_color']
            var_color= f"{varient.product_id.pr_id}-{varient_color}"

            varient_color_img=request.FILES.get('varient_color_img')
            varient_quantity=request.POST['varient_quantity']
            varient_images=request.POST.getlist('varient_images')
            
            varient.varient_id=var_color

            if varient.varient_color:
                varient.varient_color.delete()
            varient.varient_color=varient_color_img

            qun=varient.product_id.total_quantity-varient.quantity
            varient.quantity=varient_quantity
            

            new_images=images.objects.filter(id__in=varient_images)

            varient.image_field.set(new_images)
            
            varient.save()

            # quantity upation ---------------------------- start
            qun =qun + int(varient.quantity)
            pro_qun=product.objects.get(id=varient.product_id.id)
            pro_qun.total_quantity=qun
            pro_qun.save()

            #  quantity updation end-------------------------------

        return render(request,'varient_update.html',{"varients":varient,"image_data":img})
    except Exception as e:
        return HttpResponse(e)




#  ------------------------------------------UPDATING VARIENT IMAGES -------------------------
#    
def image_update(request,varient_id):
    try:
        img=images.objects.all().order_by('-id')
        varient=verients.objects.select_related('product_id').get(id=varient_id)
        if request.method == 'POST' and request.FILES.getlist('varient_images'):
            varient_images=request.FILES.getlist('varient_images')
            owner=request.POST['owner']
            v=images.objects.order_by('-id').first()
            if v.owner == owner:
                messages.info(request,'Try another name to understand !')
                return render(request,'varient_update.html',{"varients":varient,"image_data":img})
            for i in varient_images:
                new_file=images(image_1=i,owner=owner)
                new_file.save()
            return render(request,'varient_update.html',{"varients":varient,"image_data":img})
        else:
            return render(request,'varient_update.html',{"varients":varient,"image_data":img})
    except Exception as e:
        return HttpResponse(e)
    



# ----------------------------------------MULTIPLE IMAGES FOR THE VARIENT -----------------------------------

def varient_img_add(request):
    try:
        if request.method == 'POST' and request.FILES.getlist('varient_images'):
            varient_images=request.FILES.getlist('varient_images')
            owner=request.POST['owner']
            v=images.objects.order_by('-id').first()
            if v.owner == owner:
                messages.info(request,'Try another name to understand !')
                return redirect(varient)
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
    


# ----------------------------------------------------------UPDATING BRAND--------------------------------------
from PIL import Image
def update_brand(request,brand_id):
   try:
     brandd=brand.objects.get(id=brand_id)
     if request.method == 'POST':
         brand_name=request.POST['brand_name']
         if brand.objects.filter(brand_name__iexact=brand_name).exclude(id=brand_id).exists():
             messages.info(request,'Brand Name already excits!')
             return render(request,'brand_update.html',{'brandd':brandd})
         brand_image=request.FILES.get('brand_image')
         if brand_image:
            brandd.brand_image.delete()
         brandd.brand_image=brand_image
         brandd.brand_name=brand_name
         brandd.save()
         return redirect(brands)
        

     return render(request,'brand_update.html',{'brandd':brandd})      
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
    except Exception as e:          # try:
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
    
# -----------------------------------------------UPDATE CATEGORY ------------------------------------------------
def update_category(request,category_id):
    try:
        try:
            catego=category.objects.get(id=category_id)
        except:
            messages.info(request,'Category not Found !')
        if request.method == 'POST':
            category_name=request.POST['category_name']
            if category.objects.filter(category_name__iexact=category_name).exclude(id=category_id).exists():
                messages.info(request,'Category Already Excits !')
                return redirect(update_category,category_id)
            category.objects.filter(id=category_id).update(category_name=category_name)
            return redirect(category_)
        else:
            return render(request,'category_update.html',{"category":catego})
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
  

# ---USER MANAGEMENT ----------------------------
from user.models import *
def user_management(request):
    try:
        users=customer.objects.all().exclude(is_superuser='True').order_by('id')
        return render(request,'user_management.html',{'users':users})
    except Exception as e:
        return HttpResponse(e)
    
def user_block(request,user_id):
        userr=customer.objects.get(id=user_id)
        if userr.is_active == True:
             customer.objects.filter(id=user_id).update(is_active='False')
        else:
            customer.objects.filter(id=user_id).update(is_active='True')
        return redirect(user_management)
