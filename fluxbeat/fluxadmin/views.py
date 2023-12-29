from datetime import date
from django.shortcuts import render,HttpResponse,redirect
from fluxadmin.models import *
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import *
import time
from user.models import customeUser,order_items,orders
from django.db.models import Count

# Create your views here.
@login_required(login_url='admin_login')
def dashboard(request):
    if request.user.is_authenticated and request.user.is_superuser:
      memcount=0
      members=customeUser.objects.filter(is_superuser = False).all()
      for i in members:
          memcount +=1
      total_orders = order_items.objects.count()
      total_products = product.objects.count()
      total_earning = orders.objects.filter(Q(order_status = 'delivered') & Q(payment_id__Paymment_status = True)).aggregate(total_earning=Sum('offer_price'))['total_earning']
      total_earning = total_earning or 0
      pending = order_items.objects.filter(Q(order_status='processing') | Q(order_status='shipped')).count()
      deliverd =order_items.objects.filter(order_status = 'delivered').count()
      canceld =order_items.objects.filter(order_status ='canceld').count()
      today_orderss = orders.objects.all()
      context={
          'total_orders':total_orders,
          'total_products':total_products,
          'total_earning':total_earning,
          'pending':pending,
          'deliverd':deliverd,
          'canceld':canceld,
          'user_count':memcount,
          'users':members,
          'orders':today_orderss


      }
     
      if request.method == 'POST':
          opt=request.POST.get('opt')
          if opt == 'today':
            today_orderss = orders.objects.filter(Q(order_date=date.today()))
            context['orders']=today_orderss
            return render(request,'admindashboard.html',context)
          
          if opt == 'week':
            today_orderss =orders.objects.filter(Q(order_date__week=date.today().isocalendar()[1]))
            context['orders']=today_orderss
            return render(request,'admindashboard.html',context)
          
          if opt == 'month':
            today_orderss = orders.objects.filter(Q(order_date__month=date.today().month))
            context['orders']=today_orderss
            return render(request,'admindashboard.html',context)
          
          if opt == 'year':
            today_orderss = orders.objects.filter(Q(order_date__year=date.today().year))
            context['orders']=today_orderss
            return render(request,'admindashboard.html',context)
            
      return render(request,'admindashboard.html',context)
    else:
      return redirect(admin_login)


#   -------------------order_detailed view-------------  
@login_required(login_url='admin_login')
def order_view(request,order_id):
    try:
        if request.user.is_authenticated and request.user.is_superuser:
            order=orders.objects.get(id=order_id)
            products=order.order_itemss.all()
            return render(request,'dashboard_order_view.html',{'order':order,'items':products})
    except Exception as e:
        return HttpResponse(e)


# ----------------------------------ADDING PRODUCT -----------------------------------------
@login_required(login_url='admin_login')
def add_product(request):
    try:
       if request.user.is_authenticated and request.user.is_superuser:
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
       else:
           return redirect(admin_login)
    except Exception as e:
        return HttpResponse(e)
  

# -----------------------------------------------------EDIT PRODUCT---------------------------------------------
@login_required(login_url='admin_login')
def edit_product(request,product_id):

    try:
        if request.user.is_authenticated and request.user.is_superuser:
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
        else:
            return redirect(admin_login)

    except Exception as e:
        return HttpResponse(e)

# ----------------------------------------------------------BLOCK PRODUCT ----------------------------------------
@login_required(login_url='admin_login')
def product_block(request,product_id):
    try:
       if request.user.is_authenticated and request.user.is_superuser:
            c=product.objects.get(id=product_id)
            if c.is_active:
                c.is_active ='False'
                c.save()
            else:
                c.is_active ='True'
                c.save()

            return redirect(product_list)
       else:
           return redirect(admin_login)
    except Exception as e:
        return HttpResponse(e)


# ---------------------------------------------------------------PRODUCT LISTING -----------------------------------------
@login_required(login_url='admin_login')
def product_list(request):
    try:
        if request.user.is_authenticated and request.user.is_superuser:
            verient=verients.objects.all().order_by('id')
            products = product.objects.select_related('category_id', 'brand_id').all()
            return render(request,'page-products-list.html',{'products':products,"verient":verient})
        else:
            return redirect(admin_login)
    except Exception as e:
        return HttpResponse(e)


# ------------------------------------------- VARIENT MANAGEMENT ------------------------------------------
@login_required(login_url='admin_login')
def varient(request):
    try:
        if request.user.is_authenticated and request.user.is_superuser:
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
        else:
            return redirect(admin_login)
    except Exception as e:
        return HttpResponse(e)
    

# ----------------------------------------   UPDATE VARIENT --------------------------------------------
@login_required(login_url='admin_login')
def update_varient(request,varient_id):
    try:
        if request.user.is_authenticated and request.user.is_superuser:
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
        else:
            return redirect(admin_login)
    except Exception as e:
        return HttpResponse(e)




#  ------------------------------------------UPDATING VARIENT IMAGES -------------------------
@login_required(login_url='admin_login')  
def image_update(request,varient_id):
    try:
        if request.user.is_authenticated and request.user.is_superuser:
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
        else:
            return redirect(admin_login)
    except Exception as e:
        return HttpResponse(e)
    



# ----------------------------------------MULTIPLE IMAGES FOR THE VARIENT -----------------------------------
@login_required(login_url='admin_login')
def varient_img_add(request):
    try:
        if request.user.is_authenticated and request.user.is_superuser:
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
        else:
            return redirect(admin_login)
    except Exception as e:
        return HttpResponse(e)
    




# ------------------------------------------BRAND MANAGEMENT ---------------------------------------

from .forms import ImageForm,CategoryForm
from .models import brand,category
@login_required(login_url='admin_login')
def brands(request):
    try:
        if request.user.is_authenticated and request.user.is_superuser:
                b_data=brand.objects.all().order_by('id')
                if request.method == 'POST':
                     form = ImageForm(request.POST, request.FILES)
                     if form.is_valid():
                        form.save()
                        return redirect(brands)
                else:
                    form = ImageForm()

                    return render(request, 'page-brands.html',{"form": form,'c':b_data})
        else:
            return redirect(admin_login)

    except Exception as e:
        return HttpResponse(e)
    


# ----------------------------------------------------------UPDATING BRAND--------------------------------------
from PIL import Image
@login_required(login_url='admin_login')
def update_brand(request,brand_id):
   try:
     if request.user.is_authenticated and request.user.is_superuser:
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
     else:
         return redirect(admin_login) 
   except Exception as e:
       return HttpResponse(e)
        
    

# ---------------------------------------------------------------------BRAND BLOCKER----------------------------------
@login_required(login_url='admin_login')
def brand_blocker(request,brand_id):
    try:
        if request.user.is_authenticated and request.user.is_superuser:
                current_brand=brand.objects.get(id=brand_id)
                if current_brand.is_active == True:
                    brand.objects.filter(id=brand_id).update(is_active='False')
                else:
                    brand.objects.filter(id=brand_id).update(is_active='True')
                return redirect(brands)
        else:
            return redirect(admin_login)
    except Exception as e:          # try:
        return HttpResponse(e)
   


# -------------------------------------------------------- CATEGORY MANAGEMENT --------------------------------------
@login_required(login_url='admin_login')
def category_(request):
    try:
       if request.user.is_authenticated and request.user.is_superuser:
            c_data=category.objects.all().order_by('id')
            if request.method == 'POST':
                form=CategoryForm(request.POST)
                if form.is_valid():
                
                    form.save()
                    return redirect(category_)
            else:
                 form=CategoryForm()
            return render(request,'page-categories.html',{"category_form":CategoryForm,"category_data":c_data})
       else:
           return redirect(admin_login)
    except Exception as e:
        return HttpResponse(e)
    
# -----------------------------------------------UPDATE CATEGORY ------------------------------------------------
@login_required(login_url='admin_login')
def update_category(request,category_id):
    
    try:
        if request.user.is_authenticated and request.user.is_superuser:
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
        else:
            return redirect(admin_login)
    except Exception as e:
        return HttpResponse(e)
# ----------------------------------------------CATEGORY BLOCKER ------------------------------------------------
@login_required(login_url='admin_login')
def category_blocker(request,cat_id):
    try:
        if request.user.is_authenticated and request.user.is_superuser:
                category_item=category.objects.get(id=cat_id)
                if category_item.is_active == True:
                    category.objects.filter(id=cat_id).update(is_active='False')
                else:
                    category.objects.filter(id=cat_id).update(is_active='True')
                return redirect(category_)
        else:
            return redirect(admin_login)
    except Exception as e:      
        return HttpResponse(e)
   

# ----------------------------------------------- ADMMIN LOG OUT-----------------------------------------------------
def admin_logout(request):
   logout(request)
   return redirect(admin_login)

# -----------------------------------------     ADMIN LOGIN -------------------------------
def admin_login(request):
    try:
        if  request.user.is_authenticated and request.user.is_superuser:
                return redirect(dashboard)
        else:
                if request.method == 'POST':
                    email=request.POST['username']
                    pasword=request.POST['password']
                    user=authenticate(request,email=email,password=pasword)
                    if user is not None and user.is_superuser:
                        login(request,user)
                        return redirect(dashboard)
                    else:
                        messages.info(request,'Usernae or Password does not match !')
                        return redirect(admin_login)


                return render(request,'admin_login.html')
 
       
    except Exception as e:
        return HttpResponse(e)
  

# ---USER MANAGEMENT ----------------------------

@login_required(login_url='admin_login')
def user_management(request):
    try:
        if request.user.is_authenticated and request.user.is_superuser:
            users=customeUser.objects.all().exclude(is_superuser='True').order_by('id')
            return render(request,'user_management.html',{'users':users})
        else:
            return redirect(admin_login)
    except Exception as e:
        return HttpResponse(e)
    
    # ------------------------------------   BLAOCKING USER--------------------------------\

@login_required(login_url='admin_login')
def user_block(request,user_id):
        try:
            if request.user.is_authenticated and request.user.is_superuser:
                    userr=customeUser.objects.get(id=user_id)
                    if userr.is_active == True:
                         customeUser.objects.filter(id=user_id).update(is_active='False')
                    else:
                        customeUser.objects.filter(id=user_id).update(is_active='True')
                    return redirect(user_management)
            else:
                return redirect(admin_login)
        except Exception as e:
            return HttpResponse(e)
        

@login_required(login_url='admin_login')
def order_management(request):

        if request.user.is_authenticated and request.user.is_superuser:
           
            order=order_items.objects.all().order_by('-added_date')
            order_list=orders.objects.all().order_by('-id')
            return render(request,'order_management.html',{'order':order,'order_list':order_list})
        else:
            return redirect(admin_login)
        

@login_required(login_url='admin_login')
def order_detail(request,order_id):
     if request.user.is_authenticated and request.user.is_superuser:
         choices=order_items.status
         order=order_items.objects.get(id=order_id)
         if request.method == 'POST':
             order_status=request.POST.get('order_stauts')
             if order_status == 'canceld':
                 order.order_id.sub_total -= order.total_price
                 order.order_id.save()
                 order.varient_id.quantity += order.proudct_quantity
                 order.varient_id.save()
             order.order_status=order_status
             order.save()
             k=order.order_id.order_itemss.all()
             b=len(k)
             print(b)
             ss=0
             sd=0
             sc=0
             for i in k:
                 if i.order_status == 'shipped':
                     ss +=1
                 if i.order_status == 'delivered':
                     sd +=1
                 if i.order_status == 'canceld':
                    sc +=1
             if ss == b-sc:
                 print('shipped')
                 order.order_id.order_status = 'shipped'
                 order.order_id.save()
             if sd == b-sc:
                 print('deliverd')
                 order.order_id.order_status = 'delivered'
                 order.order_id.save()
             if sc == b:
                 print('cancled')
                 order.order_id.order_status = 'canceld'
                 order.sub_total = 0
                 order.order_id.save()
                    
             return redirect(order_management)
         return render(request,'page-orders-detail.html',{'order':order,'choice':choices})
     else:
        return redirect(admin_login)
     

# -------------------------------COUPON MANAGEMENT -------------------------
from .forms import couponform
def coupon_management(request):
    try:
        coupones=coupon.objects.all()
        if request.method == 'POST':
            form =couponform(request.POST)
            if form.is_valid():
                form.save()
                return redirect(coupon_management)
            else:
            # Form is not valid, add error messages to the messages framework
                form_data = request.POST
                for errors in form.errors.items():
                    for error in errors:
                        messages.info(request,error)
                    return render(request,'coupon_mangement.html',{"form":form,'coupon':coupones,'form_data': form_data})
        form = couponform()
        return render(request,'coupon_mangement.html',{"form":form,'coupon':coupones})
    except Exception as e:
        return HttpResponse(e)