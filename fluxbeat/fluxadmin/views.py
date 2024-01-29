
from datetime import date, timedelta
import datetime
from decimal import Decimal
import decimal
from io import BytesIO
import json
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from django.shortcuts import render,HttpResponse,redirect,reverse
from fluxadmin.models import *
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import *
import time
from user.models import customeUser,order_items,orders, wallet
from django.db.models import Count
from django.views.decorators.cache import cache_control
# Create your views here.
@login_required(login_url='admin_login')
def dashboard(request):
    if request.user.is_authenticated and request.user.is_superuser:
      label=[]
      data=[]


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

            sucess_order=order_items.objects.filter(Q(order_status='delivered') & Q(added_date=date.today())).count()
            canceld_order=order_items.objects.filter(Q(order_status='canceld') & Q(added_date=date.today())).count()
            returned_order=order_items.objects.filter(Q(order_status='returned') & Q(added_date=date.today())).count()
            label.append('succes')
            data.append(sucess_order)
            label.append('canceld')
            data.append(canceld_order)
            label.append('returned')
            data.append(returned_order)
            context['label']=label
            context['data']=data
            today_orderss = orders.objects.filter(Q(order_date=date.today()))
            context['orders']=today_orderss
            return render(request,'admindashboard.html',context)
          
          if opt == 'week':

            sucess_order=order_items.objects.filter(Q(order_status='delivered') & Q(added_date__week=date.today().isocalendar()[1])).count()
            canceld_order=order_items.objects.filter(Q(order_status='canceld') & Q(added_date__week=date.today().isocalendar()[1])).count()
            returned_order=order_items.objects.filter(Q(order_status='returned') & Q(added_date__week=date.today().isocalendar()[1])).count()
            print(sucess_order)
            label.append('succes')
            data.append(sucess_order)
            label.append('canceld')
            data.append(canceld_order)
            label.append('returned')
            data.append(returned_order)
            context['label']=label
            context['data']=data
            today_orderss =orders.objects.filter(Q(order_date__week=date.today().isocalendar()[1]))
            context['orders']=today_orderss
            return render(request,'admindashboard.html',context)
          
          if opt == 'month':
            sucess_order=order_items.objects.filter(Q(order_status='delivered') & Q(added_date__month=date.today().month)).count()
            canceld_order=order_items.objects.filter(Q(order_status='canceld') & Q(added_date__month=date.today().month)).count()
            returned_order=order_items.objects.filter(Q(order_status='returned') & Q(added_date__month=date.today().month)).count()
            print(sucess_order)
            label.append('succes')
            data.append(sucess_order)
            label.append('canceld')
            data.append(canceld_order)
            label.append('returned')
            data.append(returned_order)
            context['label']=label
            context['data']=data
            today_orderss = orders.objects.filter(Q(order_date__month=date.today().month))
            context['orders']=today_orderss
            return render(request,'admindashboard.html',context)
          
          if opt == 'year':
            sucess_order=order_items.objects.filter(Q(order_status='delivered') & Q(added_date__year=date.today().year)).count()
            canceld_order=order_items.objects.filter(Q(order_status='canceld') & Q(added_date__year=date.today().year)).count()
            returned_order=order_items.objects.filter(Q(order_status='returned') & Q(added_date__year=date.today().year)).count()
            print(sucess_order)
            label.append('succes')
            data.append(sucess_order)
            label.append('canceld')
            data.append(canceld_order)
            label.append('returned')
            data.append(returned_order)
            context['label']=label
            context['data']=data
            today_orderss = orders.objects.filter(Q(order_date__year=date.today().year))
            context['orders']=today_orderss
            return render(request,'admindashboard.html',context)
          
      sucess_order=order_items.objects.filter(order_status='delivered').count()
      canceld_order=order_items.objects.filter(order_status='canceld').count()
      returned_order=order_items.objects.filter(order_status='returned').count()
      label.append('succes')
      data.append(sucess_order)
      label.append('canceld')
      data.append(canceld_order)
      label.append('returned')
      data.append(returned_order)
      context['label']=label
      context['data']=data
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
            choices = product.HEADPHONE_TYPES
            category_choice = category.objects.all()
            brand_choice = brand.objects.all()

            if request.method == 'POST':
                product_image = request.FILES.get('product_image')
                product_id = request.POST['product_id']
                product_name = request.POST['product_name']
                product_des = request.POST['product_description']
                product_price = request.POST['product_price']
                product_sale = request.POST['sale_price']
                product_type = request.POST['headphone_type']
                product_cat = request.POST['headphone_cate']
                cate_id = category.objects.get(id=product_cat)
                product_brand = request.POST['headphone_brand']
                brand_id = brand.objects.get(id=product_brand)

                try:
                    int(product_price)
                except ValueError:
                    messages.info(request, "Price should be a number!")
                    return redirect(add_product)

                try:
                    int(product_sale)
                except ValueError:
                    messages.info(request, "Sale price should be a number!")
                    return redirect(add_product)

                if int(product_price) < int(product_sale):
                    messages.info(request, 'Sale price must be lower than product price!')
                    return redirect(add_product)

                if int(product_price) <= 0 and int(product_sale) <= 0:
                    messages.info(request, 'Price should be greater than 0!')
                    return redirect(add_product)

                if product.objects.filter(Q(pr_id=product_id) | Q(product_name=product_name)).exists():
                    messages.info(request, 'Product already exists!')
                    return redirect(add_product)


                try:
                    with Image.open(product_image) as img:
                        # Crop the center of the image to a fixed size (adjust width and height as needed)
                        width, height = img.size
                        left = (width - min(width, height)) / 2
                        top = (height - min(width, height)) / 2
                        right = (width + min(width, height)) / 2
                        bottom = (height + min(width, height)) / 2

                        cropped_img = img.crop((left, top, right, bottom))

                        # Save the cropped image to a BytesIO buffer
                        buffer = BytesIO()
                        cropped_img.save(buffer, format='JPEG')
                        product_image = InMemoryUploadedFile(buffer, None, f'{product_id}.jpg', 'image/jpeg',
                                                             buffer.tell(), None)
                except Exception as e:
                    messages.info(request, "File type does not match. Try to upload an image only!")
                    return redirect(add_product)

                product_obj = product.objects.create(pr_id=product_id, product_image=product_image,
                                                     product_name=product_name, description=product_des,
                                                     product_price=product_price, sale_prce=product_sale,
                                                     headphone_type=product_type, category_id=cate_id,
                                                     brand_id=brand_id, total_quantity=0)
                product_obj.save()

                success_message = "Product added successfully!"
                return render(request, 'page-form-product-1.html',
                              {'choice': choices, 'category_choice': category_choice, 'brand_choice': brand_choice,
                               'success_message': success_message})

            success_message = False
            return render(request, 'page-form-product-1.html',
                          {'choice': choices, 'category_choice': category_choice, 'brand_choice': brand_choice,
                           'success_message': success_message})
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
                    if request.FILES.get('product_image'):
                        p=product.objects.get(id=product_id)
                        p.product_name=product_name
                        p.description=product_des
                        p.product_price=prodct_price

                        # ---------------updating the sale_price---------
                        if p.offer_applied:
                            sale_price=int(sale_price)
                            offer_per=int(p.offer_applied.offer_per)
                            discount = int(sale_price * (offer_per / 100))
                            p.offer_amount=discount
                            sale_price -= discount
                            p.sale_prce =sale_price
                        else:
                            sale_price=int(sale_price)
                            p.sale_prce=sale_price

                        p.headphone_type=prodcut_type
                        p.category_id=h_cate
                        p.brand_id=h_bran
                        if p.product_image:
                            p.product_image.delete()
                        p.product_image=product_image
                        p.save()
                    else:
                        p=product.objects.get(id=product_id)
                        p.product_name=product_name
                        p.description=product_des
                        p.product_price=prodct_price

                        # ----------updating sale price if offer is applied---------
                        if p.offer_applied:
                            sale_price=int(sale_price)
                            offer_per=int(p.offer_applied.offer_per)
                            discount = int(sale_price * (offer_per / 100))
                            p.offer_amount=discount
                            sale_price -= discount
                            p.sale_prce =sale_price
                        else:
                            sale_price=int(sale_price)
                            p.sale_prce=sale_price

                        p.headphone_type=prodcut_type
                        p.category_id=h_cate
                        p.brand_id=h_bran
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
            products = product.objects.select_related('category_id', 'brand_id').all().order_by('-pr_id')
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
                product_data=product.objects.all().order_by('-id')
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
                    
                    if request.FILES.get('varient_color_img'):
                        if varient.varient_color:
                            varient.varient_color.delete()
                        varient.varient_color=varient_color_img

                    qun=varient.product_id.total_quantity-varient.quantity
                    varient.quantity=varient_quantity

                    if request.POST.getlist('varient_images'):
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
                    try:
                        v=images.objects.order_by('-id').first()
                        if v.owner == owner:
                            messages.info(request,'Try another name to understand !')
                            return redirect(varient)
                    except Exception as e:
                        return HttpResponse(e)
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
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_logout(request):
   logout(request)
   return redirect(admin_login)

# -----------------------------------------     ADMIN LOGIN -------------------------------
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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
                if order.order_id.address:
                       address_detail=json.loads(order.order_id.address)
                else:
                        address_detail={}
                if request.method == 'POST':
                    order_status=request.POST.get('order_stauts')
                    if order_status == 'canceld':

                        next_sub_totol=order.order_id.sub_total - order.total_price
                        user_idd=order.user_id
                        main_order=orders.objects.get(id=order.order_id.id)
                        wallet_instance=wallet.objects.get(user_id=user_idd)

                        # --------if coupon is applied-------------------------
                        if main_order.offer_applied:
                            # calculating product amount and adding into the wallet----------------
                            previous_offer_price=order.order_id.offer_price
                            per=order.order_id.offer_applied.offer_per
                            discount = int(next_sub_totol * (per / 100))
                            next_offer_price=next_sub_totol - discount
                            amount_to_be_added_to_wallet = previous_offer_price - next_offer_price
                            # addin to money to the wallet end here--------------------/
                        else:
        
                            previous_offer_price = main_order.offer_price
                            next_offer_price= previous_offer_price - order.total_price
                            amount_to_be_added_to_wallet= previous_offer_price - next_offer_price

                        if main_order.payment_id.Paymment_status == True:
                            debit_histo= Decimal(amount_to_be_added_to_wallet)
                            wallet_instance.wallet_amount += Decimal(amount_to_be_added_to_wallet)
                            historyy=f"order :{order.id} canceld-amount Rs. {debit_histo} is credited to the wallet"
                            wallet_instance.append_to_string_list(historyy)
                            wallet_instance.save()
                            # adding money to the wallet if coupon is not applied end here ------------

                        order.order_id.sub_total = next_sub_totol
                        order.order_id.offer_price = next_offer_price
                        order.order_id.save()
                        # changing order subtotal amount and offer_price amount ---------------
                    


                        order.varient_id.quantity += order.proudct_quantity
                        order.varient_id.save()
                    order.order_status=order_status
                    order.save()
                    k=order.order_id.order_itemss.all()

                    # ----------changeing the payment status to true if all the order is deliveres---

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

                    # --------------setting payment of cod to true if all items are deliveres ---------------------
                    if order.order_id.order_status == 'delivered':
                        paid_amount=order.order_id.offer_price
                        order.order_id.payment_id.Paymment_status =  True
                        order.order_id.payment_id.Paymment_amount = paid_amount
                        order.order_id.payment_id.save()

                    return redirect(order_management)
                return render(request,'page-orders-detail.html',{'order':order,'choice':choices,'address':address_detail})
            else:
               return redirect(admin_login)

         
     

# -------------------------------COUPON MANAGEMENT -------------------------
from .forms import couponform
@login_required(login_url='admin_login')
def coupon_management(request):
    try:
        if request.user.is_authenticated and request.user.is_superuser:
                coupones=coupon.objects.all().order_by('id')
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
        else:
            return redirect(admin_login)
    except Exception as e:
        return HttpResponse(e)
    
    # ------------------------------EDIT COUPON-----------------
@login_required(login_url='admin_login')    
def edit_coupon(request,coupon_id):
     try:
          if request.user.is_authenticated and request.user.is_superuser:
              if request.method == 'POST':
                coupon_name=request.POST.get('coupon_name')
                code=request.POST.get('code')
                min_amount=request.POST.get('min_amount')
                offer_per=request.POST.get('offer_per')
                expiary_date = request.POST.get('expiary_date')

                data=coupon.objects.get(id=coupon_id)

                data.coupon_name=coupon_name
                data.code=code
                data.min_amount=min_amount
                data.offer_per=offer_per
                data.exp_date=expiary_date
                data.save()
                return redirect(coupon_management)
              else:
                  co_data=coupon.objects.get(id=coupon_id)
                  return render(request,'edit_coupon',{'data':co_data})
          else:
              return redirect(admin_login)
     except Exception as e:
         return HttpResponse(e)

@login_required(login_url='admin_login')    
def delete_coupon(request,coupon_id):
     try:
          if request.user.is_authenticated and request.user.is_superuser:
              coupon.objects.get(id=coupon_id).delete()
              return redirect(coupon_management)
          else:
              return redirect(admin_login)
     except Exception as e:
         return HttpResponse(e)
     
    # ------------------------------------COMPLETING RETURN --------------------    
@login_required(login_url='admin_login')
def complete_return(request,order_id):
    try:
        if request.user.is_authenticated and request.user.is_superuser:
            item=order_items.objects.get(id=order_id)
            item.order_status='returned'
            item.save()
            product_varient=verients.objects.get(id=item.varient_id.id)
            product_varient.quantity += item.proudct_quantity
            # after returnig money crediting to the wallet------------
            user_wallet=wallet.objects.get(user_id=item.user_id)
            

            # ------------adding to wallet when coupon is applied in this order ------------------
            if item.order_id.offer_applied:
                next_subtotal=item.order_id.sub_total - item.total_price
                per=item.order_id.offer_applied.offer_per
                discount = int(next_subtotal * (per / 100))
                previous_offer_price=item.order_id.offer_price
                item.order_id.sub_total= next_subtotal
                item.order_id.offer_price= next_subtotal - discount
                item.order_id.save()
            else:
                # -----------adding to wallte when coupon is not applied----------------
                next_subtotal=item.order_id.sub_total - item.total_price
                previous_offer_price=item.order_id.offer_price
                item.order_id.sub_total=next_subtotal
                item.order_id.offer_price=next_subtotal
                item.order_id.save()
                print('offer ot paller')

            # -----------adding to wallet----------------
            price_of_returned_item=  previous_offer_price - item.order_id.offer_price 
            user_wallet.wallet_amount += price_of_returned_item
            historyy=f"order :{item.order_id} canceld-amount Rs. {price_of_returned_item} is credited to the wallet"
            user_wallet.append_to_string_list(historyy)
            user_wallet.save()

            return redirect(order_management)

        else:
            return redirect(admin_login)
    except Exception as e:
        return HttpResponse(e)
    

# -----------------------DIALY SALE REPORT -----------------
@login_required(login_url='admin_login')
def daily_sale(request):
    try:
        today=date.today()
        total_order=order_items.objects.filter(added_date = today).count()
        total_sales=orders.objects.filter(order_date = today).aggregate(sum=Sum('offer_price'))
        avg_order_value=orders.objects.filter(order_date = today).aggregate(avg=Avg('offer_price'))
        k=avg_order_value['avg']
        if k:
            avg_sale=round(k,2)
        else:
            avg_sale=0
        if total_sales['sum'] == None:
            total_sales['sum'] = 0
        sold_products_today = order_items.objects.filter(added_date=today).values('proudct_id__product_name').annotate(total_quantity=Sum('proudct_quantity'))

        today_orders=order_items.objects.filter(added_date = today).all()
        context={
            'total_order':total_order,
            'total_sales':total_sales,
            'avg_order_value':avg_sale,
            'day_orders':today_orders,
            'soled_proudcts':sold_products_today
        }
        if request.user.is_authenticated and request.user.is_superuser:
            return render(request,'daily_sale.html',context)
        else:
            return redirect(admin_login)
    except Exception as e:
        return HttpResponse(e)
    

# -----------------------WEEK SALE REPORT -----------------
@login_required(login_url='admin_login')
def week_sale(request):
    try:
        today=date.today()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        iso_year, iso_week, iso_weekday = today.isocalendar()

        total_order=order_items.objects.filter(added_date__range=[start_of_week, end_of_week]).count()
        total_sales=orders.objects.filter(order_date__range=[start_of_week, end_of_week]).aggregate(sum=Sum('offer_price'))
        avg_order_value=orders.objects.filter(order_date__range=[start_of_week, end_of_week]).aggregate(avg=Avg('offer_price'))
        print(total_sales)
        k=avg_order_value['avg']
        if k:
            avg_sale=round(k,2)
        else:
            avg_sale=0
        if total_sales['sum'] == None:
            total_sales['sum'] = 0
        sold_products_today = order_items.objects.filter(added_date__range=[start_of_week, end_of_week]).values('proudct_id__product_name').annotate(total_quantity=Sum('proudct_quantity'))

        today_orders=order_items.objects.filter(added_date__range=[start_of_week, end_of_week]).all()
        context={
            'total_order':total_order,
            'total_sales':total_sales,
            'avg_order_value':avg_sale,
            'day_orders':today_orders,
            'soled_proudcts':sold_products_today,
            'week':iso_week
        }
        if request.user.is_authenticated and request.user.is_superuser:
            return render(request,'week_sale.html',context)
        else:
            return redirect(admin_login)
    except Exception as e:
        return HttpResponse(e)



# -----------------------YEAR SALE REPORT -----------------
@login_required(login_url='admin_login')
def year_sale(request):
    try:
        today=date.today()
        start_of_year = date(today.year, 1, 1)
        end_of_year = date(today.year, 12, 31)
        iso_year, iso_week, iso_weekday = today.isocalendar()

        total_order=order_items.objects.filter(added_date__range=[start_of_year, end_of_year]).count()
        total_sales=orders.objects.filter(order_date__range=[start_of_year, end_of_year]).aggregate(sum=Sum('offer_price'))
        avg_order_value=orders.objects.filter(order_date__range=[start_of_year, end_of_year]).aggregate(avg=Avg('offer_price'))
        print(total_sales)
        k=avg_order_value['avg']
        if k:
            avg_sale=round(k,2)
        else:
            avg_sale=0
        if total_sales['sum'] == None:
            total_sales['sum'] = 0
        sold_products_today = order_items.objects.filter(added_date__range=[start_of_year, end_of_year]).values('proudct_id__product_name').annotate(total_quantity=Sum('proudct_quantity'))

        today_orders=order_items.objects.filter(added_date__range=[start_of_year, end_of_year]).all()
        context={
            'total_order':total_order,
            'total_sales':total_sales,
            'avg_order_value':avg_sale,
            'day_orders':today_orders,
            'soled_proudcts':sold_products_today,
            'year':iso_year
        }
        if request.user.is_authenticated and request.user.is_superuser:
            return render(request,'year_sale.html',context)
        else:
            return redirect(admin_login)
    except Exception as e:
        return HttpResponse(e)
    
from fluxadmin.models import special_offer
def special_offerr(request):
    try:
        categoryy=category.objects.all()
        prodcutss=product.objects.all()
        special_offers=special_offer.objects.all()
        
        context={
            'category':categoryy,
            'products':prodcutss,
            'special_offer':special_offers
        }
        if request.method == 'POST':
            offer_title=request.POST.get('offer_title')
            banner_image=request.FILES.get('banner_image')
            start_date=request.POST.get('start_date')
            end_date=request.POST.get('end_date')
            offer_per=request.POST.get('offer_per')
            offer_applied_for=request.POST.get('opt')
            if offer_applied_for == 'category':
                opt_id=request.POST.get('cat_id')
            else:
                opt_id=request.POST.get('opt_name')
                     

   

            banner_width = 800
            banner_height = 200
            try:
                image = Image.open(banner_image)
            except Exception:
                messages.info(request,'upload image file')
                return redirect(special_offerr)


            # Calculate the coordinates for cropping the center part

            if start_date > end_date:
                    messages.info(request,'end date should be after start date')
                    return redirect(special_offerr)
            if special_offer.objects.filter(offer_title = offer_title).exists():
                messages.info(request,'Offer already exists')
                return redirect(special_offerr)
            offer=special_offer.objects.create(appied_for=offer_applied_for,namee=opt_id,offer_title=offer_title,banner_image=banner_image,stat_date=start_date,end_date=end_date,offer_per=offer_per)
            offer.save()


        # ------croping the image-------------
            try:
                image = Image.open(banner_image)
            except Exception:
                messages.info(request, 'Upload image file')
                return redirect(special_offerr)

            # Resize and crop the image
            resized_image = image.resize((banner_width, banner_height))
            left = (resized_image.width - banner_width) // 2
            top = (resized_image.height - banner_height) // 2
            right = (resized_image.width + banner_width) // 2
            bottom = (resized_image.height + banner_height) // 2

            cropped_image = resized_image.crop((left, top, right, bottom))

            # Save the cropped image to a BytesIO buffer
            buffer = BytesIO()
            cropped_image.save(buffer, format="JPEG")  # You can change the format as needed

            # Create a new ImageField instance for the database model
            offer.banner_image.save(banner_image.name, buffer)

            # Save other details to the database
            offer.save()

            # ------------croping end here---------------


            # -------applying special offer to products under category-------
            if offer_applied_for == 'category':
                category_instance=category.objects.get(id=opt_id)
                product_under_category=category_instance.category_products.all()
                print(category_instance)

                # -------cheching if offer is already applied------------
                for i in product_under_category:
                    if i.offer_applied:
                        if i.offer_applied.offer_per > int(offer.offer_per):
                            continue
                        else:
                            discount=i.offer_amount
                            i.sale_prce += discount
                            i.save()

                    product_price=i.sale_prce
                    per=int(offer.offer_per)
                    discount = int(product_price * (per / 100))
                    i.offer_amount=discount
                    i.sale_prce -= discount
                    i.offer_applied=offer
                    i.save()
                return redirect(special_offerr)
            
            # -------------APPLYING OFFER TO PROUDCT---------
            elif offer_applied_for == 'product':
                product_instance=product.objects.get(id=opt_id)

                # ----------checking if offer is already applied--------

                if product_instance.offer_applied:
                    if product_instance.offer_applied.offer_per > int(offer.offer_per):
                        offer.delete()
                        messages.info(request,'already an offer applied')
                        return redirect(special_offerr)
                    else:
                        discount=product_instance.offer_amount
                        product_instance.sale_prce += discount
                        product_instance.save()

                product_price = product_instance.sale_prce
                per = Decimal(offer.offer_per)
                discount = int(product_price * (per / 100))
                product_instance.offer_amount=discount
                product_instance.sale_prce -= discount
                product_instance.offer_applied=offer
                product_instance.save()

            m=f"special offer created ,and applied to products"
            messages.info(request,m)
            return redirect(special_offerr)
        return render(request,'special_offer.html',context)
    except Exception as e:
        return HttpResponse(e)
    

def special_offer_delete(request,offer_id):
    try:
        if request.user.is_authenticated and request.user.is_superuser:
            special_offer_applied=special_offer.objects.get(id=offer_id)
            if special_offer_applied.appied_for == 'category':
                category_instance=category.objects.get(id=special_offer_applied.namee)
                product_under_category=category_instance.category_products.all()
                if product_under_category:
                    for i in product_under_category:
                        #  ---checking if offer is applied-
                         if i.offer_applied:
                            if i.offer_applied.id == special_offer_applied.id:
                                discount=i.offer_amount
                                i.sale_prce += discount
                                i.offer_amount = None
                                i.offer_applied = None
                                i.save()
                special_offer_applied.delete()
                return redirect(special_offerr)
            elif special_offer_applied.appied_for == 'product':
        
                     product_instance=product.objects.get(id=special_offer_applied.namee)
                    #  ----------checking if offer is applied----
                     if product_instance.offer_applied:
                        if product_instance.offer_applied.id == special_offer_applied.id:
                            discount=product_instance.offer_amount
                            product_instance.sale_prce += discount
                            product_instance.offer_amount = None
                            product_instance.offer_applied = None
                            product_instance.save()
                     special_offer_applied.delete()

                     return redirect(special_offerr)
    except Exception as e:
        return HttpResponse(e)

def edit_special_offer(request,offer_id):

        if request.user.is_authenticated and request.user.is_superuser:
           categoryy=category.objects.all()
           prodcutss=product.objects.all()
           offer=special_offer.objects.get(id=offer_id)
           if offer.appied_for == 'category':
               a=category.objects.get(id=offer.namee)
               applied_for_name=a.category_name

           elif offer.appied_for == 'product':
               a=product.objects.get(id=offer.namee)
               applied_for_name=a.product_name
           id=int(offer.id)
        #    ---------UPDATION------------
           if request.method == 'POST':
                offer_title=request.POST.get('offer_title')
                banner_image=request.FILES.get('banner_image')
                start_date=request.POST.get('start_date')
                end_date=request.POST.get('end_date')
                offer_per=request.POST.get('offer_per')
                offer_applied_for=request.POST.get('opt')
                
                if offer_applied_for == 'category':
                    opt_id=request.POST.get('cate_id')
                else:
                    opt_id=request.POST.get('opt_name')
               
                offer_instance = special_offer.objects.get(id=offer_id)
                if start_date > end_date:
                    messages.info(request,'end date should be after start date')
                    return redirect(reverse('edit_special_offer' ,args=[offer_id]))
                
                if special_offer.objects.filter(offer_title = offer_title).exclude(id=offer_id).exists():
                    messages.info(request,'Offer with same offer title already exists!')
                    return redirect(reverse('edit_special_offer' ,args=[offer_id]))
                
                if request.FILES.get('banner_image'):
                    offer_instance.banner_image.delete()
                    offer_instance.banner_image = banner_image
                    offer_instance.save()

                previous_offer_per=offer_instance.offer_per

                offer=special_offer.objects.get(id=offer_id)
                offer.offer_title=offer_title
                offer.stat_date=start_date
                offer.end_date=end_date
                offer.offer_per=offer_per
                offer.save()
                # changing the product price if percentage is changed-------
                if int(previous_offer_per) != int(offer.offer_per):
                    print('not ')
                    offer_per=int(offer.offer_per)
                    if offer.appied_for == 'category':
                        category_instance=category.objects.get(id=offer.namee)
                        products_under_category=category_instance.category_products.all()
                        if products_under_category:
                            for i in products_under_category:
                                product_sale_price= int(i.sale_prce + i.offer_amount)
                                discount = int(product_sale_price * (offer_per / 100))
                                i.sale_prce = product_sale_price - discount
                                i.offer_amount=discount
                                i.save()
                    elif offer.appied_for == 'product':
                        product_instance = product.objects.get(id=offer.namee)
                        if product_instance.offer_applied:
                            product_sale_price = int(product_instance.sale_prce + product_instance.offer_amount)
                            discount = int(product_sale_price * (offer_per /100 ))
                            product_instance.sale_prce = product_sale_price - discount
                            product_instance.offer_amount = discount
                            product_instance.save()

                return redirect(special_offerr)
                

           return render(request,'special_offer_edit.html',{'offer':offer,'category':categoryy,'products':prodcutss,'id':id,'applied_for_name':applied_for_name})
        else:
            return redirect(admin_login)
