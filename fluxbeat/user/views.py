from django.shortcuts import render,HttpResponse,redirect,reverse
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
from datetime import timedelta
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User=get_user_model()
# Create your views here.
def home(request):
    try:
            if request.user.is_authenticated and not request.user.is_superuser:
                c=1
            else:
                c=0
      
            products=product.objects.select_related('brand_id','category_id').annotate(offer=ExpressionWrapper(F('product_price') - F('sale_prce'),output_field=models.DecimalField( ))).order_by('id')
            arrival=product.objects.select_related('brand_id','category_id').annotate(offer=ExpressionWrapper(F('product_price') - F('sale_prce'),output_field=models.DecimalField( ))).order_by('product_date')
            brands=brand.objects.all()
            return render(request,'index.html',{"products":products,"brands":brands,"arrival":arrival,'login_status':c})
        
    except Exception as e:
        return HttpResponse(e)


# USER REGISTRATION AND VALIDATION........................................................................-----------------
import re
def user_reg(request):
    try:
         if request.method=='POST':
             first_name=request.POST['firstname']
             last_name=request.POST['lastname']
             email=request.POST['email']
             phoneno=request.POST['phoneno']
             password=request.POST['password']
             cpassword=request.POST['cpassword']

             request.session['first_name']=first_name
             request.session['last_name']=last_name
             request.session['email']=email
             request.session['phoneno']=phoneno
             request.session['password']=password
             password_pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
             if password != cpassword:
                messages.info(request,'password does not match !')
                return redirect(user_reg)
             elif not re.match(password_pattern,password):
                 messages.info(request,'Password is not Strong!')
                 return redirect(user_reg)
             elif not re.match(r'^[A-Za-z]+(?: [A-Za-z]+)?$',first_name):
                 messages.info(request,'Enter a valid first name !')
                 return redirect(user_reg)
             elif len(phoneno) !=  10:
                 messages.info(request,'Enter a valid Phone number !')
                 return redirect(user_reg)
             if User.objects.filter(email=email).exists():
                messages.info(request,'Email already exist !')
                return redirect(user_reg)
             try:
               email_validator = EmailValidator(message="Enter a valid email address.")
               email_validator(email)
            # email validation--------------------------------
             except ValidationError as e:
                 error_message = e.message
                 messages.info(request,error_message)
                 return redirect(user_reg)
             if not first_name or not last_name or not email or not phoneno or not password or not cpassword:
                 messages.info(request,'All feilds must be filled !')
                 return redirect(user_reg)
             
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
       return render(request,'otp.html')
    except Exception as e:
        return HttpResponse(e)



# ----------------------------------USER LOGIN ----------------------------
def user_signin(request):
    try:
         
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
                  request.session.clear()
                  return redirect(user_signin)
              else:
                  messages.info(request,'Invalid OTP')
                  return render(request,'otp.html')
            else:
                messages.info(request,'Time limit is exceeded !')
                return render(request,'otp.html')
    except Exception as e:
        return HttpResponse(e)
    


# ---------------------------------------- PRODUCT DETAIELS ------------------------

def product_detail(request,product_id):
    try:
        if request.user.is_authenticated and not request.user.is_superuser:
                c=1
        else:
                c=0
        productt=product.objects.get(id=product_id)
        offer=productt.product_price - productt.sale_prce
        current=productt.product_varients.all().first()
        varientss=productt.product_varients.all()
        imagess=current.image_field.all().order_by('-id')
        return render(request,'product_detail.html',{'product':productt,'varients':varientss,'images':imagess,'offer':offer,'current':current,'login_status':c})
    except Exception as e:
        return HttpResponse(e)
    

# ---------------------------------------------------CHANGE VARIENT --------------------------------

def varient_change(request,product_id,varient_id):
    try:
        if request.user.is_authenticated and not request.user.is_superuser:
                c=1
        else:
                c=0
        productt=product.objects.get(id=product_id)
        offer=productt.product_price - productt.sale_prce
        current=verients.objects.get(id=varient_id)
        varientss=productt.product_varients.all()
        imagess=current.image_field.all().order_by('-id')
        return render(request,'product_detail.html',{'product':productt,'varients':varientss,'images':imagess,'offer':offer,'current':current,'login_status':c})
    except Exception as e:
        return HttpResponse(e)
    


# -----------------------------------------------USER ACCOUNT ----------------------------------------
@login_required(login_url='user_signin')
def user_account(request):
    try:
        user_order=orders.objects.filter(user_id=request.user).all().order_by('-order_date')
        order_itemss=order_items.objects.all()
        user_address=address.objects.filter(user_id=request.user.id)
        if request.user.is_authenticated and not request.user.is_superuser:
                c=1
        else:
                c=0
        user=request.user
        try:
            user=User.objects.get(id=user.id)
        except:
            print("Something went wrong")
        return render(request,'page-account.html',{'login_status':c,'user':user,'user_addresses':user_address,'user_order':user_order,'order_items':order_itemss})
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
                 if npassword == "" and cpassword ==  "":
                     User.objects.filter(id=user_id).update(first_name=first_name,last_name=last_name,phone_number=phone_number)
                     return redirect(user_account)
                 else:
                     if npassword != cpassword:
                         messages.info(request,'password does not match !')
                         return redirect(user_account)
                     elif not re.match(password_pattern,npassword):
                          messages.info(request,'Password is not Strong!')
                          return redirect(user_account)
                     elif not re.match(r'^[A-Za-z]+(?: [A-Za-z]+)?$',first_name):
                          messages.info(request,'Enter a valid first name !')
                          return redirect(user_account)
                     User.objects.filter(id=user_id).update(first_name=first_name,last_name=last_name,phone_number=phone_number,password=make_password(npassword))
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
            productt=product.objects.get(id=product_id)
            if varient_id == 0:
                current_varient=productt.product_varients.all().first()
            else:
                current_varient=verients.objects.get(id=varient_id)
            userr=User.objects.get(id=request.user.id)
            if cart.objects.filter(Q(user_id=userr) & Q(proudct_id=productt) & Q(varient_id=current_varient)).exists():
                return redirect(home)
            cart.objects.create(user_id=userr,proudct_id=productt,varient_id=current_varient)
            return redirect(view_cart)
        else:
            return redirect(user_signin)
    except Exception as e:
        return HttpResponse(e)



# -----------------------------------------VIEW CART --------------------------

@login_required(login_url='user_signin')
def view_cart(request):
    try:
        if request.user.is_authenticated and not request.user.is_superuser:
            c=1
            cart_items=cart.objects.filter(user_id=request.user.id).all()
            sum=0
            for i in cart_items:
                sum +=i.total_price
            return render(request,'shop-cart.html',{'login_status':c,'cart_itmes':cart_items,'grand_total':sum})
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
                    return redirect('user_account')

                return render(request, 'add_address.html',{'login_status':c})
    except Exception as e:
        return HttpResponse(e)
    


# --------------------------------------------------------DELETE ADDRESS ---------------------------
@login_required(login_url='user_signin')
def delete_address(request,address_id):
    try:
         if request.user.is_authenticated and not request.user.is_superuser:
             address.objects.filter(id=address_id).delete()
             return redirect(user_account)
    except Exception as e:
        return HttpResponse(e)
    


# -----------------------------------------   EDIT ADDRESSS--------------------------

@login_required(login_url='user_signin')
def edit_address(request,address_id):
    try:
        if request.user.is_authenticated and not request.user.is_superuser:
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
                    return redirect(user_account)
            return render(request,'edit_address.html',{'login_status':1,'address':current_address})
        else:
            return render(user_signin)
    except Exception as e:
        return HttpResponse(e)
    


from .models import *
# -----------------   CHEKCK OUT -------------------------------------------
@login_required(login_url='user_signin')
def check_out(request):
    try:
        c=1

        user_address=address.objects.filter(user_id=request.user.id)
        cart_items=cart.objects.filter(user_id=request.user.id).all()
        sum=0
        for i in cart_items:
            sum +=i.total_price

        if request.user.is_authenticated and not request.user.is_superuser:
                if request.method == 'POST':
                    # --------------------------- address settting part start --------------------

                    if request.POST.get('address') =='add_address':
                        fname = request.POST.get('fname')
                        lname = request.POST.get('lname')
                        cname = request.POST.get('cname')
                        country = request.POST.get('country')
                        addres = request.POST.get('shipping_address')
                        address_2 = request.POST.get('shipping_address_2')
                        city = request.POST.get('city')
                        state = request.POST.get('state')
                        zipcode = request.POST.get('zipcode')
                        phone  = request.POST.get('phoneno')
                        address_type = request.POST.get('address_type')
                        if not fname or not lname or not cname or not country or not addres or not address_2 or not city or not state or not zipcode or not address_type or not phone:
                            messages.info(request,'All the fields must be filled !')
                            return redirect(check_out)
                        if len(phone) !=10:
                            messages.info(request,'Enter a valid Phone Numer')
                            return redirect(check_out)
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
                        
                    else:
                        order_address_id=request.POST.get('address')
                        ADDRESS=address.objects.get(id=order_address_id)
                    # -----------------------address setting part end ---------------------------------------
                    
                    # -----------------------------Paymment setting part start here-------------------
                    payment_type=request.POST.get('payment_option')
                    if payment_type == 'cash on delivery':
                        order_payment=Paymment.objects.create(Paymment_type=payment_type)
                    print(order_payment)
                    # -------------------------------Paymment setting part end here ---------------------

                    # -------------------------order settin part start here---------------
                    add_inform=request.POST.get('add_inform')
                    print(add_inform)
                 
                    order_idd=orders.objects.create(user_id=request.user,address_id=ADDRESS,sub_total=sum,offer_price=0,payment_id=order_payment,add_information=add_inform)


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
                        qun=i.varient_id.quantity -1
                        verients.objects.filter(id=i.varient_id.id).update(quantity=qun)
                        order_itemss.save()
                        cart_items.delete()
                    return render(request,'succes.html',{'order':order_idd,'login_status':1})

                return render(request,'shop-checkout.html',{'cart_items':cart_items,'user_addresses':user_address,'sum':sum,'login_status':c})
        else:
            return render(user_signin)
    except Exception as e:
        return HttpResponse(e)
    


# ----------------------------------------CANCEL ORDER-------------------------------------
def cancel_order(request,order_id,order_type):
    try:
         if request.user.is_authenticated and not request.user.is_superuser:
             
            #  ---------------------------------canceling each product in that purchase-------------------
             if order_type == 'order':
                 order=order_items.objects.get(id=order_id)
                 order.order_status='canceld'
                 order.save()
                 p=order.order_id.sub_total - order.total_price
                 orders.objects.filter(id=order.order_id.id).update(sub_total=p)
                 print(order.order_id)
                 k=order.order_id.order_itemss.all()
                 b=0
                 for i in k:
                     if i.order_status != 'canceld':
                         b=1
                 if b == 0:
                    cart_order=order.order_id
                    cart_order.order_status = 'canceld'
                    cart_order.save()

                 return redirect(user_account)
             
            # ---------------------------------- cancelling the all project in that purchase------------------------------
             if order_type == 'all':
                 order=orders.objects.get(id=order_id)
                 order.order_status = 'canceld'
                 order.sub_total = 0
                 order.save()
                 b=order.order_itemss.all()
                 for i in b:
                     i.order_status = 'canceld'
                     i.save()
                 return redirect(user_account)
         else:
             return redirect(user_signin)
    except Exception as e:
        return HttpResponse(e)
    

def order_detailes(request,order_id):
    c=1
    order=order_items.objects.get(id=order_id)
    return render(request,'view_order.html',{'login_status':1,'order':order})



# views.py
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from fluxadmin.models import cart

def update_cart_quantity(request, cart_item_id, operation):
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

    # Prepare data for the JSON response
    data = {
        'quantity': cart_item.proudct_quantity,
        'total_price': float(cart_item.total_price),
    }

    return JsonResponse(data)
