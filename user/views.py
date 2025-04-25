import datetime
import json
from django.shortcuts import render,HttpResponse,redirect,reverse,HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
import random
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
import time
from django.db.models import *
from fluxadmin.models import *
from datetime import date, timedelta
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from decimal import Decimal
from user.models import wishlist
User=get_user_model()
from user.models import referal
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_control
from django.conf import settings
# Create your views here.


# -------------------------SHOP PRODUCT LIST---------------------------------------------------------------------------
    
def shop_product_list(request):
  try:
            if request.user.is_authenticated and not request.user.is_superuser:
                wishlist_count=wishlist.objects.filter(user_id=request.user.id).count()
                cart_count=cart.objects.filter(user_id=request.user.id).count()
                c=1
            else:
                wishlist_count=0
                cart_count=0
                c=0
      
            products=product.objects.select_related('brand_id','category_id').annotate(offer=ExpressionWrapper(F('product_price') - F('sale_prce'),output_field=models.DecimalField( ))).order_by('id')
            arrival=product.objects.select_related('brand_id','category_id').annotate(offer=ExpressionWrapper(F('product_price') - F('sale_prce'),output_field=models.DecimalField( ))).order_by('product_date')[:4]
            brands=brand.objects.all()
            categorie=category.objects.all()


            # set pagination------
            p = Paginator(products,7)
            page = request.GET.get('page')
            product_list =p.get_page(page)


            return render(request,'shop-list-left.html',{"products":product_list,"brands":brands,"arrival":arrival,'login_status':c,'cat':categorie,'w':wishlist_count,'c':cart_count})
        
  except Exception as e:
        return HttpResponse(e)




def home(request):
    try:
            if request.user.is_authenticated and not request.user.is_superuser:
                c=1
                wishlist_count=wishlist.objects.filter(user_id=request.user.id).count()
                cart_count=cart.objects.filter(user_id=request.user.id).count()
            else:
                wishlist_count=0
                cart_count=0
                c=0
            banners=special_offer.objects.all()
            banner_count=special_offer.objects.all().count()
            if banner_count >=2:
                banner_1 = special_offer.objects.all()[:1]
                banner_2 = special_offer.objects.all()[1:2]
               
            else:
                banner_1=[]
                banner_2=[]

            # deletin offers which are out of date-------------
                

            for offer in banners:
                end_date=offer.end_date
                print(end_date)
                current_date = date.today()
                print(current_date)
                if current_date > end_date:
                          if offer.appied_for == 'category':
                             category_instance=category.objects.get(id=offer.namee)
                             product_under_category=category_instance.category_products.all()
                             if product_under_category:
                                    for i in product_under_category:
                              #  ---checking if offer is applied-
                                            if i.offer_applied:
                                                if i.offer_applied.id == offer.id:
                                                    discount=i.offer_amount
                                                    i.sale_prce += discount
                                                    i.offer_amount = None
                                                    i.offer_applied = None
                                                    i.save()
                             offer.delete()
                          elif offer.appied_for == 'product':
                          
                               product_instance=product.objects.get(id=offer.namee)
                              #  ----------checking if offer is applied----
                               if product_instance.offer_applied:
                                  if product_instance.offer_applied.id == offer.id:
                                      discount=product_instance.offer_amount
                                      product_instance.sale_prce += discount
                                      product_instance.offer_amount = None
                                      product_instance.offer_applied = None
                                      product_instance.save()
                               offer.delete()

                  # deletin offers which are out of date-------------end
                     


            top_sell=order_items.objects.values('proudct_id').annotate(item_count=Count('proudct_id')).order_by('-item_count')[:4]
            top_sell_data = []
            for i in top_sell:
              product_id = i.get('proudct_id')
              order_count = i.get('item_count')
              print(product_id)
              product_instance =product.objects.get(id=product_id)
              top_sell_data.append({
                  'product_instanc': product_instance,
                  'order_count': order_count,
              })

              for j in top_sell_data:
                  print(j['product_instanc'].product_name)

       


            products=product.objects.select_related('brand_id','category_id').annotate(offer=ExpressionWrapper(F('product_price') - F('sale_prce'),output_field=models.DecimalField( ))).order_by('id')
            arrival=product.objects.select_related('brand_id','category_id').annotate(offer=ExpressionWrapper(F('product_price') - F('sale_prce'),output_field=models.DecimalField( ))).order_by('product_date')
            brands=brand.objects.all()
            return render(request,'index.html',{"products":products,"brands":brands,"arrival":arrival,'login_status':c,'top_selling':top_sell_data,'w':wishlist_count,'c':cart_count,'banner':banners,'banner_count':banner_count
                                                ,'banner1':banner_1,'banner2':banner_2})
        
    except Exception as e:
        return HttpResponse(e)
    



# -------------------------SEARCHING PRODUCT----------------
def search_product(request):
    try:
        if request.user.is_authenticated and not request.user.is_superuser:
            c=1
            wishlist_count=wishlist.objects.filter(user_id=request.user.id).count()
            cart_count=cart.objects.filter(user_id=request.user.id).count()
        else:
            wishlist_count=0
            cart_count=0
            c=0
        brands=brand.objects.all()
        arrival=product.objects.select_related('brand_id','category_id').annotate(offer=ExpressionWrapper(F('product_price') - F('sale_prce'),output_field=models.DecimalField( ))).order_by('product_date')[:4]

        if request.method == 'POST':
                search_data=request.POST.get('search_code')
               
                matching_products = product.objects.filter(product_name__icontains=search_data)
                request.session['search_data']=search_data
                p = Paginator(matching_products,7)
                page = request.GET.get('page')
                product_list =p.get_page(page)
                categorie=category.objects.all()
                return render(request,'shop-list-left.html',{"products":product_list,"brands":brands,"arrival":arrival,'login_status':c,'cat':categorie,'w':wishlist_count,'c':cart_count})
        else:
                search_data=request.session['search_data']
                matching_products = product.objects.filter(product_name__icontains=search_data)
                p = Paginator(matching_products,7)
                page = request.GET.get('page')
                product_list =p.get_page(page)
                categorie=category.objects.all()
                return render(request,'shop-list-left.html',{"products":product_list,"brands":brands,"arrival":arrival,'login_status':c,'cat':categorie,'w':wishlist_count,'c':cart_count})
    except Exception as e:
        return HttpResponse(e)
   


# USER REGISTRATION AND VALIDATION........................................................................-----------------
import re
def user_reg(request):
    try:
          if request.user.is_authenticated and not request.user.is_superuser:
             return redirect(home)
          else:
             if request.method=='POST':
                 first_name=request.POST['firstname']
                 last_name=request.POST['lastname']
                 email=request.POST['email']
                 phoneno=request.POST['phoneno']
                 password=request.POST['password']
                 cpassword=request.POST['cpassword']
                 referal_code=request.POST['referal_code']
                 b={'fname':first_name,'lname':last_name,'email':email,'phone':phoneno}
                 request.session['first_name']=first_name
                 request.session['last_name']=last_name
                 request.session['email']=email
                 request.session['phoneno']=phoneno
                 request.session['password']=password

                 if 'referal_code' in request.session:
                            referal_code_value = request.session.pop('referal_code')

                 if request.POST['referal_code']:
                    if not referal.objects.filter(code=referal_code).exists():

                        messages.info(request,'Referal Code invalid !')
                        return render(request,'user_reg.html',b)
                    
                    request.session['referal_code']=referal_code

                 password_pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
                 if password != cpassword:
                    messages.info(request,'password does not match !')
                    return render(request,'user_reg.html',b)
                 
                 elif not re.match(password_pattern,password):
                     messages.info(request,'Password is not Strong!')
                     return render(request,'user_reg.html',b)
                 
                 elif not re.match(r'^[A-Za-z]+(?: [A-Za-z]+)?$',first_name):
                     messages.info(request,'Enter a valid first name !')
                     return render(request,'user_reg.html',b)
                 
                 elif len(phoneno) !=  10:
                     messages.info(request,'Enter a valid Phone number !')
                     return render(request,'user_reg.html',b)
                 
                 elif User.objects.filter(email=email).exists():
                    messages.info(request,'Email already exist !')
                    return render(request,'user_reg.html',b)
                 
                 elif User.objects.filter(phone_number=phoneno).exists():
                    messages.info(request,'Phone Number already in use !')
                    return render(request,'user_reg.html',b)
                 
                 try:
                   email_validator = EmailValidator(message="Enter a valid email address.")
                   email_validator(email)
                # email validation--------------------------------
                 except ValidationError as e:
                     error_message = e.message
                     messages.info(request,error_message)
                     return render(request,'user_reg.html',b)
                 if not first_name or not last_name or not email or not phoneno or not password or not cpassword:
                     messages.info(request,'All feilds must be filled !')
                     return render(request,'user_reg.html',b)
                 
                 return redirect(send_otp)
                    
             else: 
                return render(request,'user_reg.html')
    except  Exception as e:
        return HttpResponse(e)



# OTP SENDER CODE--------------------------------------------------------------------------------
def  send_otp(request):
    try:
    #    otp genarations----------------
       s=""
       for x in range(0,4):
           s+=str(random.randint(0,9))
       request.session['otp']=s
    #    otp sending--------------------------------
       send_mail("FLUXBEAT OTP VARIFICATION ",f"Your OTP of for SignUp is {s}",'fluxbeatauth@gmail.com',[request.session['email']],fail_silently=False)
       otp_gen_time=time.time()
       request.session['otp_time']=otp_gen_time
       return render(request,'otp.html',{'k':0})
    except Exception as e:
        return HttpResponse(e)



# ----------------------------------USER LOGIN ----------------------------
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_signin(request):
    try:
          if request.user.is_authenticated and not request.user.is_superuser:
             return redirect(home)
          else:
             if request.method=='POST':
                 email=request.POST['email']
                 password=request.POST['password']
                 try:
                    user=User.objects.get(email=email)
                 except Exception as e:
                   messages.info(request,'Username of Password does not match')
                   return redirect(user_signin)
                 if user.is_active == False:
                     messages.info(request,'Your account is currently blocked !')
                     return redirect(user_signin)
                 user=authenticate(request,email=email,password=password)
                 if user is not None and not user.is_superuser:
                       login(request,user)
                       return redirect(home)

                 else:
                       messages.info(request,'Email or Password does not match !')
                       return redirect(user_signin)

             return render(request,'user_login.html')

    except Exception as e:
        return HttpResponse(e)
   

# ----------------------------------------USER LOGOUT --------------------------------------------------
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_logout(request):
    logout(request)
    return redirect(home)




# OTP VARIFICATION CODE-----------------------------------------------------------------------------
def otp_varify(request):  
    try:     
        if request.method=='POST':
            # otp validating-----------------
            otp_=request.POST['otp']
            otpgen_time=request.session['otp_time']

            # time validation-------------
            if otpgen_time and (time.time() - otpgen_time) < 60:
              
              if request.session['otp']==otp_:
                  user=User.objects.create_user(first_name=request.session['first_name'],last_name=request.session['last_name'],email=request.session['email'],phone_number=request.session['phoneno'],password=request.session['password'])
                  user.save()

                  referal.objects.create(user_id=user)

                  current_wallet=wallet.objects.create(user_id=user,wallet_amount=0)

                  if 'referal_code' in request.session:
                       current_wallet.wallet_amount += 200
                       historyy=f"₹200 credited to account as referal bonus !"
                       current_wallet.append_to_string_list(historyy)
                       current_wallet.save()

                  request.session.clear()
                  return redirect(user_signin)
              else:
                  messages.info(request,'Invalid OTP')
                  return render(request,'otp.html',{'k':0})
            else:
                messages.info(request,'Time limit is exceeded !')
                return render(request,'otp.html',{'k':1})
    except Exception as e:
        return HttpResponse(e)
    


# ---------------------------------------- PRODUCT DETAIELS ------------------------

def product_detail(request,product_id):
    try:
        if request.user.is_authenticated and not request.user.is_superuser:
                wishlist_count=wishlist.objects.filter(user_id=request.user.id).count()
                cart_count=cart.objects.filter(user_id=request.user.id).count()
                c=1
        else:
                wishlist_count=0
                cart_count=0
                c=0
        productt=product.objects.get(id=product_id)
        related_products=product.objects.filter(Q(brand_id=productt.brand_id) & Q(category_id=productt.category_id))
        offer=productt.product_price - productt.sale_prce
        current=productt.product_varients.all().first()
        varientss=productt.product_varients.all()
        imagess=current.image_field.all().order_by('-id')
        return render(request,'product_detail.html',{'product':productt,'varients':varientss,'images':imagess,'offer':offer,'current':current,'login_status':c,'w':wishlist_count,'c':cart_count,'related_products':related_products})
    except Exception as e:
        return HttpResponse(e)
    

# ---------------------------------------------------CHANGE VARIENT --------------------------------

def varient_change(request,product_id,varient_id):
    try:
        if request.user.is_authenticated and not request.user.is_superuser:
                wishlist_count=wishlist.objects.filter(user_id=request.user.id).count()
                cart_count=cart.objects.filter(user_id=request.user.id).count()
                c=1
        else:
                wishlist_count=0
                cart_count=0
                c=0
        productt=product.objects.get(id=product_id)
        offer=productt.product_price - productt.sale_prce
        current=verients.objects.get(id=varient_id)
        varientss=productt.product_varients.all()
        imagess=current.image_field.all().order_by('-id')
        return render(request,'product_detail.html',{'product':productt,'varients':varientss,'images':imagess,'offer':offer,'current':current,'login_status':c,'w':wishlist_count,'c':cart_count})
    except Exception as e:
        return HttpResponse(e)
    


# -----------------------------------------------USER ACCOUNT ----------------------------------------

@login_required(login_url='user_signin')
def user_account(request):
    try:
        try:
            wallets=wallet.objects.get(user_id=request.user.id)
        except:
            usr=customeUser.objects.get(id=request.user.id)
            wallets=wallet.objects.create(user_id=usr,wallet_amount=0)
        try:
            referal_instance =referal.objects.get(user_id=request.user.id)
            referal_id=referal_instance.code
        except:
            usr=customeUser.objects.get(id=request.user.id)
            referal_instance =referal.objects.create(user_id=usr)
            referal_id=referal_instance.code


        wallet_history=wallets.get_string_list()
        reversed_wallet_history = list(reversed(wallet_history))
        print(wallet_history)
        user_order=orders.objects.filter(user_id=request.user).all().order_by('-id')
        order_itemss=order_items.objects.all()
        user_address=address.objects.filter(user_id=request.user.id)
        if request.user.is_authenticated and not request.user.is_superuser:
                wishlist_count=wishlist.objects.filter(user_id=request.user.id).count()
                cart_count=cart.objects.filter(user_id=request.user.id).count()
                c=1
        else:
                c=0
        user=request.user
        try:
            user=User.objects.get(id=user.id)
        except:
            print("Something went wrong")
        return render(request,'page-account.html',{'login_status':c,'user':user,'user_addresses':user_address,'user_order':user_order,'order_items':order_itemss,'wallet':wallets,'w':wishlist_count,'c':cart_count,"history":reversed_wallet_history,"referal_id":referal_id})
    except Exception as e:
        return HttpResponse(e)
    
# -------------------------------------------USER UPDATION ------------------------------------------------/

@login_required(login_url='user_signiin')
def user_update(request,user_id):
    try:
        if request.user.is_authenticated and not request.user.is_superuser:
             password_pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
             if request.method == 'POST':
                 user=User.objects.get(id=user_id)
                 first_name=request.POST['first_name']
                 last_name=request.POST['last_name']
                 phone_number=request.POST['phoneno']
                 cpassword=request.POST['cpassword']
                 npassword=request.POST['npassword']
                 email=request.POST['email']
                 if npassword == "" and cpassword ==  "":
                     User.objects.filter(id=user_id).update(first_name=first_name,last_name=last_name,phone_number=phone_number)
                     return redirect(user_account)
                 else:
                     if npassword != cpassword:
                         messages.info(request,'password does not match !', extra_tags='user-update')
                         return redirect(user_account)
                     elif not re.match(password_pattern,npassword):
                          messages.info(request,'Password is not Strong!', extra_tags='user-update')
                          return redirect(user_account)
                     elif not re.match(r'^[A-Za-z]+(?: [A-Za-z]+)?$',first_name):
                          messages.info(request,'Enter a valid first name !', extra_tags='user-update')
                          return redirect(user_account)
                     b=User.objects.filter(id=user_id).update(first_name=first_name,last_name=last_name,phone_number=phone_number,password=make_password(npassword))
                     return redirect(user_account)
        else:
            return redirect(user_signin)
    except Exception as e:
        return HttpResponse(e)




# ---------------------------------------ADD TO CART------------------------------------------
@login_required(login_url='user_signin')
def add_to_cart(request,product_id,varient_id):
    try:
        if request.user.is_authenticated and not request.user.is_superuser:
            wishlist_count=wishlist.objects.filter(user_id=request.user.id).count()
            cart_count=cart.objects.filter(user_id=request.user.id).count()
            products=product.objects.select_related('brand_id','category_id').annotate(offer=ExpressionWrapper(F('product_price') - F('sale_prce'),output_field=models.DecimalField( ))).order_by('id')
            arrival=product.objects.select_related('brand_id','category_id').annotate(offer=ExpressionWrapper(F('product_price') - F('sale_prce'),output_field=models.DecimalField( ))).order_by('product_date')
            brands=brand.objects.all()
            productt=product.objects.get(id=product_id)

            banners=special_offer.objects.all()
            banner_count=special_offer.objects.all().count()
            if banner_count >=2:
                banner_1 = special_offer.objects.all()[:1]
                banner_2 = special_offer.objects.all()[1:2]
               
            else:
                banner_1=[]
                banner_2=[]

            if varient_id == 0:
                current_varient=productt.product_varients.all().first()
            else:
                current_varient=verients.objects.get(id=varient_id)
            userr=User.objects.get(id=request.user.id)
            if cart.objects.filter(Q(user_id=userr) & Q(proudct_id=productt) & Q(varient_id=current_varient)).exists():
                    already = "All ready in cart !"
                    return render(request,'index.html',{"products":products,"brands":brands,"arrival":arrival,'login_status':1,'success_message':already,'w':wishlist_count,'c':cart_count,'banner':banners,'banner_count':banner_count,'banner1':banner_1,'banner2':banner_2})
            if current_varient.quantity  == 0:


                # ----------------sweet alert for items
                stock_over = "Out of stock !"
                return render(request,'index.html',{"products":products,"brands":brands,"arrival":arrival,'login_status':1,'success_message':stock_over,'w':wishlist_count,'c':cart_count,'banner':banners,'banner_count':banner_count,'banner1':banner_1,'banner2':banner_2})
            
            cart.objects.create(user_id=userr,proudct_id=productt,varient_id=current_varient)
            return redirect(home)
        else:
            return redirect(user_signin)
    except Exception as e:
        return HttpResponse(e)



# -----------------------------------------VIEW CART --------------------------

@login_required(login_url='user_signin')
def view_cart(request):
    try:
        if request.user.is_authenticated and not request.user.is_superuser:
            wishlist_count=wishlist.objects.filter(user_id=request.user.id).count()
            cart_count=cart.objects.filter(user_id=request.user.id).count()
            c=1
            cart_items=cart.objects.filter(user_id=request.user.id).all()
            sum=0
            for i in cart_items:
                sum +=i.total_price
            return render(request,'shop-cart.html',{'login_status':c,'cart_itmes':cart_items,'grand_total':sum,'w':wishlist_count,'c':cart_count})
        else:
            return redirect(user_signin)
    except Exception as e:
        return HttpResponse(e)

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST





# ------------------------------------------------------------DELTEe CART ----------------------

@login_required(login_url='user_signin')
def delete_cart(request,cart_id):
    try:
        if request.user.is_authenticated and not request.user.is_superuser:
            cart.objects.filter(id=cart_id).delete()
            return redirect(view_cart)
        else:
            return redirect(user_signin)
    except Exception as e:
        return HttpResponse(e)
    






# ------------------------------------------ ADD ADDRESS------------------------------

from .models import address
@login_required(login_url='user_signin')
def add_address(request):
    try:
            if request.user.is_authenticated and not request.user.is_superuser:
                wishlist_count=wishlist.objects.filter(user_id=request.user.id).count()
                cart_count=cart.objects.filter(user_id=request.user.id).count()
                c=1
               
                if request.method == 'POST':
                    
                    fname = request.POST.get('fname')
                    lname = request.POST.get('lname')
                    cname = request.POST.get('cname')
                    country = request.POST.get('country')
                    addres = request.POST.get('shipping_address')
                    address_2 = request.POST.get('shipping_address_2')
                    city = request.POST.get('city')
                    state = request.POST.get('state')
                    zipcode = request.POST.get('zipcode')
                    phone = request.POST.get('phone')
                    address_type = request.POST.get('address_type')
                    if len(phone) !=10:
                        messages.info(request,'Enter a valid phone number')
                        return redirect(add_address)
                    ADDRESS=address.objects.create(
                        user_id=request.user,
                        first_name=fname,
                        last_name=lname,
                        company_name=cname,
                        country=country,
                        address=addres,
                        address_2=address_2,
                        city=city,
                        state=state,
                        pin=zipcode,
                        phone=phone,
                        address_type=address_type
                    )
                    url= reverse('user_account') + '#address'
                    print(url)
                    return HttpResponseRedirect(url)

                return render(request, 'add_address.html',{'login_status':c,'w':wishlist_count,'c':cart_count})
    except Exception as e:
        return HttpResponse(e)
    


# --------------------------------------------------------DELETE ADDRESS ---------------------------
@login_required(login_url='user_signin')
def delete_address(request,address_id):
    try:
         if request.user.is_authenticated and not request.user.is_superuser:
             address.objects.filter(id=address_id).delete()
             url = reverse('user_account') + '#address'
             return HttpResponseRedirect(url)
         
    except Exception as e:
        return HttpResponse(e)
    


# -----------------------------------------   EDIT ADDRESSS--------------------------

@login_required(login_url='user_signin')
def edit_address(request,address_id):
    try:
        if request.user.is_authenticated and not request.user.is_superuser:
            wishlist_count=wishlist.objects.filter(user_id=request.user.id).count()
            cart_count=cart.objects.filter(user_id=request.user.id).count()
            current_address=address.objects.get(id=address_id)
            if request.method == 'POST':
                    
                    fname = request.POST.get('fname')
                    lname = request.POST.get('lname')
                    cname = request.POST.get('cname')
                    country = request.POST.get('country')
                    addres = request.POST.get('shipping_address')
                    address_2 = request.POST.get('shipping_address_2')
                    city = request.POST.get('city')
                    state = request.POST.get('state')
                    zipcode = request.POST.get('zipcode')
                    phone = request.POST.get('phone')
                    address_type = request.POST.get('address_type')
                    if len(phone) != 10:
                        messages.info(request,'Enter a valid Phone Numer')
                        return redirect(reverse('edit_address' ,args=[address_id]))
                    address.objects.filter(id=address_id).update(
                        user_id=request.user,
                        first_name=fname,
                        last_name=lname,
                        company_name=cname,
                        country=country,
                        address=addres,
                        address_2=address_2,
                        city=city,
                        state=state,
                        pin=zipcode,
                        phone=phone,
                        address_type=address_type
                    )
                    url = reverse('user_account') + '#address'
                    return HttpResponseRedirect(url)
            return render(request,'edit_address.html',{'login_status':1,'address':current_address,'w':wishlist_count,'c':cart_count})
        else:
            return render(user_signin)
    except Exception as e:
        return HttpResponse(e)
    






from .models import *

# ---------------------------------------APPLY COUPON0------------------------------
@login_required(login_url='user_signin')
def apply_coupon(request):
    try:
        if request.method == 'POST':
            couponcode=request.POST.get('couponcode')
            try:
                coupon_data=coupon.objects.get(code=couponcode)
            except:
                messages.info(request,'Invalid coupon code!')
                return redirect(check_out)
            cart_items=cart.objects.filter(user_id=request.user.id).all()
            sum=0
            for i in cart_items:
              sum +=i.total_price  
            if int(sum) < coupon_data.min_amount:
                messages.info(request,'This order is not eligible for this offer!')
                return redirect(check_out)
            user_orders=orders.objects.filter(user_id=request.user.id).all()
            for i in user_orders:
                if i.offer_applied_id == coupon_data.id:
                    messages.info(request,'You have already used this coupon ,sorry !')
                    return redirect(check_out)
            
            discount = int(sum * (coupon_data.offer_per / 100))
            t_price=sum-discount
            request.session['dis_amount']=str(discount)
            request.session['t_price']=str(t_price)
            request.session['couponcode']=couponcode

            return redirect(check_out)
            
    
    except Exception as e:
        return HttpResponse(e)

# -------------------------------------------REMOVE COUPON -------------------------
@login_required(login_url='user_signin')
def remove_coupon(request):
    request.session.pop('dis_amount')
    request.session.pop('t_price')
    request.session.pop('couponcode')
    return redirect(check_out)
# -----------------   CHEKCK OUT -------------------------------------------



@login_required(login_url='user_signin')
def check_out(request):

        c=1
        current_date = date.today()
        cuponess=coupon.objects.filter(exp_date__gte=current_date)
        user_address=address.objects.filter(user_id=request.user.id)
        cart_items=cart.objects.filter(user_id=request.user.id).all()
        try:
            or_id=orders.objects.all().order_by('-id').first()
            or_idd=or_id.id + 1
        except:
            or_idd=1
        used=orders.objects.filter(user_id=request.user.id)
        used_coupons=[]
        for i in used:
            used_coupons.append(i.offer_applied)
        print(used_coupons)
        
        sum=0
        for i in cart_items:
            sum +=i.total_price

        if request.user.is_authenticated and not request.user.is_superuser:
                wishlist_count=wishlist.objects.filter(user_id=request.user.id).count()
                cart_count=cart.objects.filter(user_id=request.user.id).count()
                if request.method == 'POST':
                    print('dfsdkfljsdjfsldjflsldfkl')
                    # ----------- ---------------- address settting part start --------------------
                    print(request.POST.get('fname'))
                   
                    if request.POST.get('address') =='add_address':
                        add=request.POST.get('address')
                        fname = request.POST.get('fname')
                        lname = request.POST.get('lname')
                        cname = request.POST.get('cname')
                        country = request.POST.get('country')
                        addres = request.POST.get('shipping_address')
                        address_2 = request.POST.get('shipping_address_2')
                        city = request.POST.get('city')
                        state = request.POST.get('state')
                        zipcode = request.POST.get('zipcode')
                        phone  = request.POST.get('phone')
                        address_type = request.POST.get('address_type')
                        b={'fname':fname,'lname':lname,'cname':cname,'country':country,'add1':addres,'add2':address_2,
                           'city':city,
                           'state':state,
                           'pin':zipcode,
                           'phone':phone,
                           'address_type':address_type,
                           'add':add}
                        
                        if not fname or not lname or not cname or not country or not addres or not address_2 or not city or not state or not zipcode or not address_type or not phone:
                            message='All field must be filled !'

                            if 'dis_amount' in request.session and 'couponcode' in request.session and 't_price' in request.session:
                                        cc=coupon.objects.get(code=request.session['couponcode'])
                                        offer_percentage=cc.offer_per

                                        return render(request,'shop-checkout.html',{'cart_items':cart_items,'user_addresses':user_address,'sum':request.session['t_price'],'login_status':c,'or_id':or_idd,'coupon':cuponess,
                                                                'dis_amount':request.session['dis_amount'],'couponcode':request.session['couponcode'],
                                                                't_price':sum,'offer_per':offer_percentage,'message':message,'l':b,'w':wishlist_count,'c':cart_count,'used':used_coupons,'razorpay_key':settings.RAZORPAY_KEY})                            
                          
                            return render(request,'shop-checkout.html',{'cart_items':cart_items,'user_addresses':user_address,'sum':sum,'login_status':c,'l':b,'message':message,'or_id':or_idd,'coupon':cuponess,'w':wishlist_count,'c':cart_count,'used':used_coupons,'razorpay_key':settings.RAZORPAY_KEY})
                        

                        if len(phone) !=10:
                            message='Phone Number is not Valid!'
                            if 'dis_amount' in request.session and 'couponcode' in request.session and 't_price' in request.session:
                                        cc=coupon.objects.get(code=request.session['couponcode'])
                                        offer_percentage=cc.offer_per

                                        return render(request,'shop-checkout.html',{'cart_items':cart_items,'user_addresses':user_address,'sum':request.session['t_price'],'login_status':c,'or_id':or_idd,'coupon':cuponess,
                                                                'dis_amount':request.session['dis_amount'],'couponcode':request.session['couponcode'],
                                                                't_price':sum,'offer_per':offer_percentage,'message':message,'l':b,'w':wishlist_count,'c':cart_count,'used':used_coupons,'razorpay_key':settings.RAZORPAY_KEY})
                            
                            return render(request,'shop-checkout.html',{'cart_items':cart_items,'user_addresses':user_address,'sum':sum,'login_status':c,'l':b,'message':message,'or_id':or_idd,'coupon':cuponess,'w':wishlist_count,'c':cart_count,'used':used_coupons,'razorpay_key':settings.RAZORPAY_KEY})
                    

                        ADDRESS=address.objects.create(
                            user_id=request.user,
                            first_name=fname,
                            last_name=lname,
                            company_name=cname,
                            country=country,
                            address=addres,
                            address_2=address_2,
                            city=city,
                            state=state,
                            pin=zipcode,
                            address_type=address_type,
                            phone=phone
                        )
                        details = {
                                        'first_name':ADDRESS.first_name,
                                        'last_name': ADDRESS.last_name,
                                        'company_name': ADDRESS.company_name,
                                        'country': ADDRESS.country,
                                        'address': ADDRESS.address,
                                        'city': ADDRESS.city,
                                        'state': ADDRESS.state,
                                        'pin': ADDRESS.pin,
                                        'phone': ADDRESS.phone,
                                }
                        details_json = json.dumps(details)
                        
                    else:
                        order_address_id=request.POST.get('address')
                        ADDRESS=address.objects.get(id=order_address_id)
                        details = {
                                        'first_name':ADDRESS.first_name,
                                        'last_name': ADDRESS.last_name,
                                        'company_name': ADDRESS.company_name,
                                        'country': ADDRESS.country,
                                        'address': ADDRESS.address,
                                        'city': ADDRESS.city,
                                        'state': ADDRESS.state,
                                        'pin': ADDRESS.pin,
                                        'phone': ADDRESS.phone,
                                }
                        details_json = json.dumps(details)
                    # -----------------------address setting part end ---------------------------------------
                    
                    # -----------------------------Paymment setting part start here-------------------
                    payment_type=request.POST.get('payment_option')
                    if payment_type == 'cash on delivery':
                        order_payment=Paymment.objects.create(Paymment_type=payment_type)




                    # payment for paypal -------------
                    elif payment_type == 'paypal':
                        # --checking if the offer is applied if applied then paid amount is amount amount after dicounting offerprice--
                        if 'dis_amount' in request.session and 'couponcode' in request.session and 't_price' in request.session:
                            paidamount=request.session['t_price']
                            order_payment=Paymment.objects.create(Paymment_type=payment_type,Paymment_status=True,Paymment_amount=paidamount)
                        else:
                             order_payment=Paymment.objects.create(Paymment_type=payment_type,Paymment_status=True,Paymment_amount=sum)


            # ---------------payment for wallet -------------
                    elif payment_type =='wallet_pay':
                        wallet_amountt=wallet.objects.get(user_id=request.user.id)
                        if 'dis_amount' in request.session and 'couponcode' in request.session and 't_price' in request.session:
                            paidamount=Decimal(request.session['t_price'])
                            if wallet_amountt.wallet_amount < int(paidamount):
                                if request.POST.get('address') =='add_address':
                                    ADDRESS.delete()
                                # eroor message -----------------
                                if request.POST.get('address') =='add_address':
                                    message='Insufficient wallet balance !'
                                    if 'dis_amount' in request.session and 'couponcode' in request.session and 't_price' in request.session:
                                            cc=coupon.objects.get(code=request.session['couponcode'])
                                            offer_percentage=cc.offer_per

                                            return render(request,'shop-checkout.html',{'cart_items':cart_items,'user_addresses':user_address,'sum':request.session['t_price'],'login_status':c,'or_id':or_idd,'coupon':cuponess,
                                                                    'dis_amount':request.session['dis_amount'],'couponcode':request.session['couponcode'],
                                                                    't_price':sum,'offer_per':offer_percentage,'message':message,'l':b,'w':wishlist_count,'c':cart_count,'used':used_coupons,'razorpay_key':settings.RAZORPAY_KEY})

                                    return render(request,'shop-checkout.html',{'cart_items':cart_items,'user_addresses':user_address,'sum':sum,'login_status':c,'l':b,'message':message,'or_id':or_idd,'coupon':cuponess,'w':wishlist_count,'c':cart_count,'used':used_coupons,'razorpay_key':settings.RAZORPAY_KEY})
                                else:
                                        messages.info(request,'Insufficient wallet balance !')
                                        return redirect(check_out)
                            # ---erro message end here--------

                            order_payment=Paymment.objects.create(Paymment_type=payment_type,Paymment_status=True,Paymment_amount=paidamount)
                            wallet_amountt.wallet_amount -= int(paidamount)
                            wallet_amountt.save()
                        else:
                            if wallet_amountt.wallet_amount < sum:
                                if request.POST.get('address') =='add_address':
                                    ADDRESS.delete()
                                # eroor message -----------------
                                if request.POST.get('address') =='add_address':
                                    message='Insufficient wallet balance !'
                                    if 'dis_amount' in request.session and 'couponcode' in request.session and 't_price' in request.session:
                                            cc=coupon.objects.get(code=request.session['couponcode'])
                                            offer_percentage=cc.offer_per

                                            return render(request,'shop-checkout.html',{'cart_items':cart_items,'user_addresses':user_address,'sum':request.session['t_price'],'login_status':c,'or_id':or_idd,'coupon':cuponess,
                                                                    'dis_amount':request.session['dis_amount'],'couponcode':request.session['couponcode'],
                                                                    't_price':sum,'offer_per':offer_percentage,'message':message,'l':b,'w':wishlist_count,'c':cart_count,'used':used_coupons,'razorpay_key':settings.RAZORPAY_KEY})

                                    return render(request,'shop-checkout.html',{'cart_items':cart_items,'user_addresses':user_address,'sum':sum,'login_status':c,'l':b,'message':message,'or_id':or_idd,'coupon':cuponess,'w':wishlist_count,'c':cart_count,'used':used_coupons,'razorpay_key':settings.RAZORPAY_KEY})
                                else:
                                        messages.info(request,'Insufficient wallet balance !')
                                        return redirect(check_out)
                            order_payment=Paymment.objects.create(Paymment_type=payment_type,Paymment_status=True,Paymment_amount=sum)
                            wallet_amountt.wallet_amount -= sum
                            wallet_amountt.save()
              

                       
                            





                    # -------------------------------Paymment setting part end here ---------------------

                    # -------------------------order settin part start here---------------
                    add_inform=request.POST.get('add_inform')
                    if 'dis_amount' in request.session and 'couponcode' in request.session and 't_price' in request.session:
                        # -------order creting if the coupon is applied---------------------
                        sum_total=request.session['t_price']
                        couponcode=request.session['couponcode']
                        offer_id=coupon.objects.get(code=couponcode)
                        discount_amount=request.session['dis_amount']
                        order_idd=orders.objects.create(offer_applied_id=offer_id.id,discount_amount=discount_amount,user_id=request.user,address=details_json,sub_total=sum,offer_price=sum_total,payment_id=order_payment,add_information=add_inform)
                        
                    else:
                        # ---------------if coupon is not applied--------------------------------
                        order_idd=orders.objects.create(user_id=request.user,address=details_json,sub_total=sum,offer_price=sum,payment_id=order_payment,add_information=add_inform)

    # -------------------------------deleting the coupon sessionn---------------------- 
                    if 'dis_amount' in request.session and 'couponcode' in request.session and 't_price' in request.session:
                        request.session.pop('t_price')
                        request.session.pop('couponcode')
                        request.session.pop('dis_amount')
                    # ------------------------------------------order setting part end here ------------------------------

                    
                    for i in cart_items:
                        order_itemss=order_items(
                            order_id=order_idd,
                            user_id=i.user_id,
                            proudct_id=i.proudct_id,
                            varient_id=i.varient_id,
                            proudct_quantity=i.proudct_quantity,
                            total_price=i.total_price
                        )
                        qun=i.varient_id.quantity - i.proudct_quantity
                        verients.objects.filter(id=i.varient_id.id).update(quantity=qun)
                        order_itemss.save()
                        cart_items.delete()
                        a=order_idd.id
                    if payment_type == 'paypal':
                        return JsonResponse({'status': 'success', 'message': 'Payment confirmed','order_Id':a})
                    
                    # ----------------adding wallet hisoty--------
                    if payment_type =='wallet_pay':
                            
                            wallet_amountt=wallet.objects.get(user_id=request.user.id)
                            historyy=f"order id:{order_idd.id} order placed using wallet pay-amount Rs. {order_idd.offer_price} is debited from the wallet"
                            print(historyy)
                            wallet_amountt.append_to_string_list(historyy)
                            wallet_amountt.save()

                    return redirect(reverse('success',args=[order_idd.id]))
                
                # ------------if coupon is applied --------------------------
                if 'dis_amount' in request.session and 'couponcode' in request.session and 't_price' in request.session:
                    cc=coupon.objects.get(code=request.session['couponcode'])
                    offer_percentage=cc.offer_per
                    return render(request,'shop-checkout.html',{'cart_items':cart_items,'user_addresses':user_address,'sum':request.session['t_price'],'login_status':c,'or_id':or_idd,'coupon':cuponess,
                                                                'dis_amount':request.session['dis_amount'],'couponcode':request.session['couponcode'],
                                                                't_price':sum,'offer_per':offer_percentage,'w':wishlist_count,'c':cart_count,'used':used_coupons,'razorpay_key':settings.RAZORPAY_KEY})
                # ------------------if coupon is not applied-----------------
                return render(request,'shop-checkout.html',{'cart_items':cart_items,'user_addresses':user_address,'sum':sum,'login_status':c,'or_id':or_idd,'coupon':cuponess,'w':wishlist_count,'c':cart_count,'used':used_coupons,'razorpay_key':settings.RAZORPAY_KEY})
        else:
            return render(user_signin)

    
     
# -=---------------------------------SUCCES PAGE------------------

@login_required(login_url='user_signin') 
def success(request,order_id):
    try:
        order_idd=orders.objects.get(id=order_id)
        if request.user.is_authenticated and not request.user.is_superuser:
            wishlist_count=wishlist.objects.filter(user_id=request.user.id).count()
            cart_count=cart.objects.filter(user_id=request.user.id).count()
            return render(request,'succes.html',{'order':order_idd,'login_status':1,'w':wishlist_count,'c':cart_count})
    except Exception as e:
        return HttpResponse(e)















# ----------------------------------------CANCEL ORDER-------------------------------------
@login_required(login_url='user_signin')
def cancel_order(request,order_id,order_type):
    try:
         if request.user.is_authenticated and not request.user.is_superuser:
             
            #  ---------------------------------canceling each product in that purchase-------------------
             if order_type == 'order':
                 order=order_items.objects.get(id=order_id)
                 order.order_status='canceld'
                 order.varient_id.quantity += order.proudct_quantity
                 order.varient_id.save()
                 order.save()
                #  ----------------------------------if the offer is applied --------------
                 if order.order_id.offer_applied:
                    gg=order.order_id.offer_price
                    p=order.order_id.sub_total - order.total_price
                    per=order.order_id.offer_applied.offer_per
                    discount = int(p * (per / 100))
                    t_price=p-discount
                    order.order_id.sub_total=p
                    order.order_id.offer_price=t_price
                    amount_to_be_added=gg-t_price
                    order.order_id.save()

                #   -----------------------------------if the order has no coupon applied----------  
                 else:

                     order.order_id.sub_total -= order.total_price
                     order.order_id.offer_price -=order.total_price
                     order.order_id.save()
                     amount_to_be_added= order.total_price
                     
                 

                #  adding money to wallet when order is cancelled0-----------
                 if order.order_id.payment_id.Paymment_status == True:
                    current_wallet=wallet.objects.get(user_id=request.user.id)
                    historyy=f"order :{order.id} canceld-amount Rs. {amount_to_be_added} is credited to the wallet"
                    current_wallet.append_to_string_list(historyy)
                    current_wallet.wallet_amount +=amount_to_be_added
                    current_wallet.save()
                    messages.info(request,'Order concelled succesfully !')




                 k=order.order_id.order_itemss.all()
                 b=0
                 for i in k:
                     if i.order_status != 'canceld':
                         b=1
                 if b == 0:
                    cart_order=order.order_id
                    cart_order.order_status = 'canceld'
                    cart_order.save()
                 url = reverse('user_account') + '#orders'
                 return HttpResponseRedirect(url)
             
            # ---------------------------------- cancelling the all project in that purchase------------------------------
             if order_type == 'all':
                 order=orders.objects.get(id=order_id)
                 order.order_status = 'canceld'

                #  adding money to wallet when order is cancelled0-----------
                 if order.payment_id.Paymment_status == True:
                    current_wallet=wallet.objects.get(user_id=request.user.id)
                    historyy=f"mulitple product order id:{order.id} canceld-amount Rs. {order.offer_price} is credited to the wallet"
                    current_wallet.append_to_string_list(historyy)
                    current_wallet.wallet_amount += order.offer_price
                    current_wallet.save()
                    messages.info(request,'Order concelled succesfully !')   

                 order.offer_price = 0
                 order.sub_total = 0
                 order.save()

                 b=order.order_itemss.all()
                #  --------setting product quantity and product status---------------
                 for i in b:
                     if not i.order_status == 'canceld':
                        i.order_status = 'canceld'
                        i.varient_id.quantity += i.proudct_quantity
                        i.varient_id.save()
                        i.save()
                 url = reverse('user_account') + '#orders'
                 return HttpResponseRedirect(url)
         else:
             return redirect(user_signin)
    except Exception as e:
        return HttpResponse(e)
    
# -------------------------------ORDER DETAILES--------------------------
@login_required(login_url='user_signin')
def order_detailes(request,order_id):
     try:
            if request.user.is_authenticated and not request.user.is_superuser:
               wishlist_count=wishlist.objects.filter(user_id=request.user.id).count()
               cart_count=cart.objects.filter(user_id=request.user.id).count()
               c=1
               order=order_items.objects.get(id=order_id)
               if order.order_id.address:
                   address_detail=json.loads(order.order_id.address)
               else:
                   address_detail={}



     

               return render(request,'view_order.html',{'login_status':1,'order':order,'w':wishlist_count,'c':cart_count,'address':address_detail})
            else:
                return redirect(user_signin)
     except Exception as e:
         return HttpResponse(e)
         
    



         



# views.py
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from fluxadmin.models import cart

# --------------------------UPDATE CART QUANTITY------------------
@login_required(login_url='user_signin')
def update_cart_quantity(request, cart_item_id, operation):
     if request.user.is_authenticated and not request.user.is_superuser:
            cart_item = get_object_or_404(cart, id=cart_item_id)

            if operation == 'increase':
                if cart_item.varient_id.quantity <= cart_item.proudct_quantity:
                    data = {
                        'error': 'Stock over',
                    }
                    return JsonResponse(data)
                cart_item.proudct_quantity += 1

            elif operation == 'decrease':
                if cart_item.proudct_quantity == 1:
                    data = {
                        'quantity': cart_item.proudct_quantity,
                        'total_price': float(cart_item.total_price),
                    }
                    return JsonResponse(data)
                cart_item.proudct_quantity -= 1

            # Update the total_price
            cart_item.total_price = cart_item.proudct_quantity * cart_item.proudct_id.sale_prce

            # Save the changes
            cart_item.save()
            total=cart_item.total_price
            # Prepare data for the JSON response
            data = {
                'quantity': cart_item.proudct_quantity,
                'total_price': total,
            }

            return JsonResponse(data)
     else:
         return redirect(user_signin)
     


# --------------VIEW WISHLIST-------------------
@login_required(login_url='user_signin')
def view_wishlist(request):
    try:
        if request.user.is_authenticated and not request.user.is_superuser:
            wishlist_count=wishlist.objects.filter(user_id=request.user.id).count()
            cart_count=cart.objects.filter(user_id=request.user.id).count()
            wishlists=wishlist.objects.filter(user_id=request.user.id)
            return render(request,'wishlist.html',{'wishlist':wishlists,'w':wishlist_count,'c':cart_count,'login_status':1})
        else:
            return redirect('user_signin')
    except Exception as e:
        return HttpResponse(e)


# -------------------------ADD TO WISHLIST------------------------
@login_required(login_url='user_signin')
def add_wishlist(request,product_id,varient_id):
    try:
        if request.user.is_authenticated and not request.user.is_superuser:
            wishlist_count=wishlist.objects.filter(user_id=request.user.id).count()
            cart_count=cart.objects.filter(user_id=request.user.id).count()
            products=product.objects.select_related('brand_id','category_id').annotate(offer=ExpressionWrapper(F('product_price') - F('sale_prce'),output_field=models.DecimalField( ))).order_by('id')
            arrival=product.objects.select_related('brand_id','category_id').annotate(offer=ExpressionWrapper(F('product_price') - F('sale_prce'),output_field=models.DecimalField( ))).order_by('product_date')
            brands=brand.objects.all()
            productt=product.objects.get(id=product_id)
            price=productt.sale_prce
            if varient_id == 0:
                current_varient=productt.product_varients.all().first()
            else:
                current_varient=verients.objects.get(id=varient_id)
            userr=User.objects.get(id=request.user.id)

            banners=special_offer.objects.all()
            banner_count=special_offer.objects.all().count()
            if banner_count >=2:
                banner_1 = special_offer.objects.all()[:1]
                banner_2 = special_offer.objects.all()[1:2]
               
            else:
                banner_1=[]
                banner_2=[]

            if wishlist.objects.filter(Q(user_id=userr) & Q(proudct_id=productt) & Q(varient_id=current_varient)).exists():
                    already_wish = "All ready in wishlist !"
                    return render(request,'index.html',{"products":products,"brands":brands,"arrival":arrival,'login_status':1,'success_message':already_wish,'w':wishlist_count,'c':cart_count,'banner':banners,'banner_count':banner_count,'banner1':banner_1,'banner2':banner_2})

            wishlist.objects.create(user_id=userr,proudct_id=productt,varient_id=current_varient,price=price)
            return redirect(home)
        else:
            return redirect(user_signin)
    except Exception as e:
        return HttpResponse(e)
    
# ---------------------REMOVEV FROM WISHLIST---------------/
def remove_wishlist(request,wishlist_id):
    try:
        if request.user.is_authenticated and not request.user.is_superuser:
            wishlist.objects.get(id=wishlist_id).delete()
            return redirect(view_wishlist)
        else:
            return redirect('user_signin')
    except Exception as e:
        return HttpResponse(e)
    


# ---------------------------------------------RETURN PRODUCT---------------------
@login_required(login_url='user_signin')
@require_POST
def req_return(request):
    try:
        if request.user.is_authenticated and not request.user.is_superuser:
            if request.method == 'POST':
                order_id=request.POST.get('order_id')
                reason=request.POST.get('reason')
                if not request.POST.get('reason'):
                    messages.info(request,'Reason should be specified !')
                    return redirect(reverse('order_detailes',args=[order_id]))
                current_order=order_items.objects.get(id=order_id)
                current_order.order_status='return_initiated'
                current_order.return_reason=reason
                current_order.save()
            return redirect(reverse('order_detailes',args=[order_id]))
        else:
            return redirect(user_signin)
    except Exception as e:
        return HttpResponse(e)
    


# ------------------ABOUT PAGE----------------------------


def about(request):
    try:
        if request.user.is_authenticated and not request.user.is_superuser:
                c=1
                wishlist_count=wishlist.objects.filter(user_id=request.user.id).count()
                cart_count=cart.objects.filter(user_id=request.user.id).count()
        else:
                wishlist_count=0
                cart_count=0
                c=0
        return render(request,'about.html',{'login_status':c,'w':wishlist_count,'c':cart_count})
    except Exception as e:
        return HttpResponse(e)
    




def sort_by(request,type):

        if request.user.is_authenticated and not request.user.is_superuser:
            wishlist_count=wishlist.objects.filter(user_id=request.user.id).count()
            cart_count=cart.objects.filter(user_id=request.user.id).count()
            c=1
        else:
            wishlist_count=0
            cart_count=0
            c=0
        if type == 'featured':
            
            return redirect(shop_product_list)
        elif type == 'lth':
            
            products=product.objects.select_related('brand_id','category_id').annotate(offer=ExpressionWrapper(F('product_price') - F('sale_prce'),output_field=models.DecimalField( ))).order_by('sale_prce')
            arrival=product.objects.select_related('brand_id','category_id').annotate(offer=ExpressionWrapper(F('product_price') - F('sale_prce'),output_field=models.DecimalField( ))).order_by('product_date')[:4]
            brands=brand.objects.all()
            categorie=category.objects.all()


            # set pagination------
            p = Paginator(products,7)
            page = request.GET.get('page')
            product_list =p.get_page(page)
            return render(request,'shop-list-left.html',{"products":product_list,"brands":brands,"arrival":arrival,'login_status':c,'cat':categorie,'w':wishlist_count,'c':cart_count})

        elif type == 'htl':
          
            products=product.objects.select_related('brand_id','category_id').annotate(offer=ExpressionWrapper(F('product_price') - F('sale_prce'),output_field=models.DecimalField( ))).order_by('-sale_prce')
            arrival=product.objects.select_related('brand_id','category_id').annotate(offer=ExpressionWrapper(F('product_price') - F('sale_prce'),output_field=models.DecimalField( ))).order_by('product_date')[:4]
            brands=brand.objects.all()
            categorie=category.objects.all()


            # set pagination------
            p = Paginator(products,7)
            page = request.GET.get('page')
            product_list =p.get_page(page)


            return render(request,'shop-list-left.html',{"products":product_list,"brands":brands,"arrival":arrival,'login_status':c,'cat':categorie,'w':wishlist_count,'c':cart_count})
       
        elif type == 'date':
   
            products=product.objects.select_related('brand_id','category_id').annotate(offer=ExpressionWrapper(F('product_price') - F('sale_prce'),output_field=models.DecimalField( ))).order_by('product_date')
            arrival=product.objects.select_related('brand_id','category_id').annotate(offer=ExpressionWrapper(F('product_price') - F('sale_prce'),output_field=models.DecimalField( ))).order_by('product_date')[:4]
            brands=brand.objects.all()
            categorie=category.objects.all()


            # set pagination------
            p = Paginator(products,7)
            page = request.GET.get('page')
            product_list =p.get_page(page)


            return render(request,'shop-list-left.html',{"products":product_list,"brands":brands,"arrival":arrival,'login_status':c,'cat':categorie,'w':wishlist_count,'c':cart_count})
       
        elif type == 'cat':
            
            products=product.objects.select_related('brand_id','category_id').annotate(offer=ExpressionWrapper(F('product_price') - F('sale_prce'),output_field=models.DecimalField( ))).order_by('product_date')
            arrival=product.objects.select_related('brand_id','category_id').annotate(offer=ExpressionWrapper(F('product_price') - F('sale_prce'),output_field=models.DecimalField( ))).order_by('product_date')[:4]
            brands=brand.objects.all()
            categorie=category.objects.all()


            # set pagination------
            p = Paginator(products,7)
            page = request.GET.get('page')
            product_list =p.get_page(page)


            return render(request,'shop-list-left.html',{"products":product_list,"brands":brands,"arrival":arrival,'login_status':c,'cat':categorie,'w':wishlist_count,'c':cart_count})
        else:
            return redirect(shop_product_list)
        


# -------------------sor by category-----------------------------
def sort_by_category(request, cat_name):
        if request.user.is_authenticated and not request.user.is_superuser:
            wishlist_count=wishlist.objects.filter(user_id=request.user.id).count()
            cart_count=cart.objects.filter(user_id=request.user.id).count()
            c=1
        else:
            wishlist_count=0
            cart_count=0
            c=0
        data=str(cat_name)
        products=product.objects.filter(category_id__category_name=data).select_related('brand_id','category_id').annotate(offer=ExpressionWrapper(F('product_price') - F('sale_prce'),output_field=models.DecimalField( ))).order_by('sale_prce')
        arrival=product.objects.select_related('brand_id','category_id').annotate(offer=ExpressionWrapper(F('product_price') - F('sale_prce'),output_field=models.DecimalField( ))).order_by('product_date')[:4]
        brands=brand.objects.all()
        categorie=category.objects.all()

          # set pagination------
        p = Paginator(products,7)
        page = request.GET.get('page')
        product_list =p.get_page(page)
        return render(request,'shop-list-left.html',{"products":product_list,"brands":brands,"arrival":arrival,'login_status':c,'cat':categorie,'w':wishlist_count,'c':cart_count})


# ------------------------------filter by price------------

def filter_by_price(request):
    try:
        if request.user.is_authenticated and not request.user.is_superuser:
            wishlist_count=wishlist.objects.filter(user_id=request.user.id).count()
            cart_count=cart.objects.filter(user_id=request.user.id).count()
            c=1
        else:
            wishlist_count=0
            cart_count=0
            c=0
        if request.method == 'POST':
            min_price = Decimal(request.POST.get('min_value', 0))
            max_price = Decimal(request.POST.get('max_value', float('inf')))

            products=product.objects.filter(Q(sale_prce__gte=min_price) & Q(sale_prce__lte=max_price)).select_related('brand_id','category_id').annotate(offer=ExpressionWrapper(F('product_price') - F('sale_prce'),output_field=models.DecimalField( ))).order_by('sale_prce')
            arrival=product.objects.select_related('brand_id','category_id').annotate(offer=ExpressionWrapper(F('product_price') - F('sale_prce'),output_field=models.DecimalField( ))).order_by('product_date')[:4]
            brands=brand.objects.all()
            categorie=category.objects.all()

            request.session['min_price']=int(min_price)
            request.session['max_price']=int(max_price)
              # set pagination------
            p = Paginator(products,7)
            page = request.GET.get('page')
            product_list =p.get_page(page)
            return render(request,'shop-list-left.html',{"products":product_list,"brands":brands,"arrival":arrival,'login_status':c,'cat':categorie,'w':wishlist_count,'c':cart_count})
        
        # -------------if request is not post then appying pagination ot the result dataset----
        else:
            min_price= Decimal(request.session['min_price'])
            max_price= Decimal(request.session['max_price'])
            products=product.objects.filter(Q(sale_prce__gte=min_price) & Q(sale_prce__lte=max_price)).select_related('brand_id','category_id').annotate(offer=ExpressionWrapper(F('product_price') - F('sale_prce'),output_field=models.DecimalField( ))).order_by('sale_prce')
            arrival=product.objects.select_related('brand_id','category_id').annotate(offer=ExpressionWrapper(F('product_price') - F('sale_prce'),output_field=models.DecimalField( ))).order_by('product_date')[:4]
            brands=brand.objects.all()
            categorie=category.objects.all()
            p = Paginator(products,7)
            page = request.GET.get('page')
            product_list =p.get_page(page)
            return render(request,'shop-list-left.html',{"products":product_list,"brands":brands,"arrival":arrival,'login_status':c,'cat':categorie,'w':wishlist_count,'c':cart_count})

            
    except Exception as e:
        return HttpResponse(e)


def privacy_policy(request):
    try:
        if request.user.is_authenticated and not request.user.is_superuser:
            wishlist_count=wishlist.objects.filter(user_id=request.user.id).count()
            cart_count=cart.objects.filter(user_id=request.user.id).count()
            c=1
        else:
            wishlist_count=0
            cart_count=0
            c=0
        return render(request,'privacy_policy.html',{'login_status':c,'w':wishlist_count,'c':cart_count})
    except Exception as e:
        return HttpResponse(e)
    
def contact_us(request):
    try:
        if request.user.is_authenticated and not request.user.is_superuser:
            wishlist_count=wishlist.objects.filter(user_id=request.user.id).count()
            cart_count=cart.objects.filter(user_id=request.user.id).count()
            c=1
        else:
            wishlist_count=0
            cart_count=0
            c=0
        return render(request,'contactus.html',{'login_status':c,'w':wishlist_count,'c':cart_count})
    except Exception as e:
        return HttpResponse(e)
    


def errorpage(request,exception=None):
    return render(request,'404.html')