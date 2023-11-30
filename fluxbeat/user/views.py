from django.shortcuts import render,HttpResponse,redirect
from django.contrib import messages
from user.models import customer
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
import random
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
import time
from fluxadmin.models import *
from datetime import timedelta
from django.contrib.auth import authenticate,login,logout
# Create your views here.
def home(request):
    try:
        products=product.objects.select_related('brand_id','category_id').order_by('product_date')[:5]
        return render(request,'home.html',{"products":products})
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
             if customer.objects.filter(email=email).exists():
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
                    user=customer.objects.get(email=email)
                 except Exception as e:
                   messages.info(request,'Username of Password does not match')
                   return redirect(user_signin)

                 if user.email == email and user.password == password and not user.is_superuser:
                       request.session['user']=user.username

                       
                       print(user.username)
                       return redirect(home)

                 else:
                       messages.info(request,'Email or Password does not match !')
                       return redirect(user_signin)

             return render(request,'user_login.html')

    except Exception as e:
        return HttpResponse(e)
   





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
                  user=customer.objects.create(first_name=request.session['first_name'],last_name=request.session['last_name'],email=request.session['email'],phoneno=request.session['phoneno'],password=request.session['password'])
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