import json
from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import userManager

# Create your models here.

class customeUser(AbstractUser):
    username= None
    email=models.EmailField(unique=True)
    phone_number=models.CharField(max_length=100,unique=True,blank=True)
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS =[]

    objects=userManager()

class address(models.Model):
    user_id=models.ForeignKey(customeUser,on_delete=models.CASCADE,related_name='user_addresses')
    first_name=models.CharField(max_length=100,null=False)
    last_name=models.CharField(max_length=100,blank=True)
    company_name=models.CharField(max_length=100,null=False)
    country=models.CharField(max_length=100,null=False)
    address=models.TextField(max_length=500,null=False)
    address_2=models.TextField(max_length=500,null=False)
    city=models.CharField(max_length=100,null=False)
    state=models.CharField(max_length=100,null=False)
    pin=models.CharField(max_length=50,null=False)
    phone=models.CharField(max_length=50,null=False)
    address_type=models.CharField(max_length=100,null=False)

    def __str__(self):
        return "Address of {first_named}"


class Paymment(models.Model):
    Paymment_type=models.CharField(max_length=100,null=False)
    Paymment_date=models.DateField(auto_now_add=True)
    Paymment_status=models.BooleanField(default=False)
    Paymment_amount=models.DecimalField(max_digits=10,decimal_places=2,null=True)

from fluxadmin.models import coupon
class orders(models.Model):
    status = [
        ('Processing', 'processing'),
        ('shipped', 'shipped'),
        ('delivered', 'delivered'),
        ('canceld','canceld')
        ]
    user_id=models.ForeignKey(customeUser,on_delete=models.CASCADE,related_name='user_orders')
    sub_total=models.DecimalField(max_digits=10, decimal_places=2)
    offer_price=models.DecimalField(max_digits=10,decimal_places=2)
    order_date=models.DateField(auto_now_add=True)
    payment_id = models.OneToOneField(Paymment, on_delete=models.CASCADE)
    order_status=models.CharField(max_length=20, choices=status, default='Processing')
    add_information=models.TextField(max_length=100,blank=True,null=True)
    discount_amount=models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True)
    offer_applied=models.ForeignKey(coupon,on_delete=models.CASCADE,related_name='offer_applied_orders',null=True)
    address=models.TextField(max_length=100)


from fluxadmin.models import product,verients
from django.core.validators import MinValueValidator
class order_items(models.Model):
    status = [
        ('Processing', 'processing'),
        ('shipped', 'shipped'),
        ('delivered', 'delivered'),
        ('canceld','canceld'),
        ('return_initiated','return_initiated'),
        ('returned','returned')
        ]
    order_id=models.ForeignKey(orders,on_delete=models.CASCADE,related_name='order_itemss')
    order_status=models.CharField(max_length=20, choices=status, default='Processing')
    user_id=models.ForeignKey(customeUser,on_delete=models.CASCADE,related_name='cartt_items',null=False)
    proudct_id=models.ForeignKey(product,on_delete=models.CASCADE,related_name='cartt_items',null=False)
    varient_id=models.ForeignKey(verients,on_delete=models.CASCADE,null=False)
    proudct_quantity=models.IntegerField(validators=[MinValueValidator(0)],
        help_text='Enter a positive integer for product quantity',default=1)
    added_date=models.DateField(auto_now_add=True)
    total_price=models.DecimalField(max_digits=10, decimal_places=2,blank=True)
    return_reason=models.TextField(null=True)
    

class wallet(models.Model):
    user_id=models.OneToOneField(customeUser,on_delete=models.CASCADE,related_name='user_wallet',unique=True)
    wallet_amount=models.DecimalField(max_digits=15,decimal_places=2,)
    history = models.TextField(null=True,default=json.dumps([]))

    def set_string_list(self, value):
        self.history = json.dumps(value)

    def get_string_list(self):
        return json.loads(self.history)
    
    def append_to_string_list(self, new_value):
        current_list = self.get_string_list()
        current_list.append(new_value)
        self.set_string_list(current_list)

    def __str__(self):
        return f"{self.user_id.first_name} wallet"



class wishlist(models.Model):
    user_id=models.ForeignKey(customeUser,on_delete=models.CASCADE,related_name='wishlist_items',null=False)
    proudct_id=models.ForeignKey(product,on_delete=models.CASCADE,related_name='list_of_wishlist',null=False)
    varient_id=models.ForeignKey(verients,on_delete=models.CASCADE,null=False)
    added_date=models.DateField(auto_now_add=True)
    price=models.DecimalField(max_digits=10, decimal_places=2,blank=True)

import random
import string
class referal(models.Model):
    user_id = models.OneToOneField(customeUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=7, null=False, unique=True)

    @staticmethod
    def referal_code_generator(length):
        characters = string.ascii_letters + string.digits
        random_string = ''.join(random.sample(characters, length))
        return random_string

    def save(self, *args, **kwargs):
        # Generate a unique 7-character code
        while True:
            unique_code = referal.referal_code_generator(length=7)
            if not referal.objects.filter(code=unique_code).exists():
                break

        self.code = unique_code
        super().save(*args, **kwargs)