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
    address_id=models.ForeignKey(address,on_delete=models.CASCADE)
    sub_total=models.DecimalField(max_digits=10, decimal_places=2)
    offer_price=models.DecimalField(max_digits=10,decimal_places=2)
    order_date=models.DateField(auto_now_add=True)
    payment_id = models.OneToOneField(Paymment, on_delete=models.CASCADE)
    order_status=models.CharField(max_length=20, choices=status, default='Processing')
    add_information=models.TextField(max_length=100,blank=True,null=True)
    discount_amount=models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True)
    offer_applied=models.ForeignKey(coupon,on_delete=models.CASCADE,related_name='offer_applied_orders',null=True)


from fluxadmin.models import product,verients
from django.core.validators import MinValueValidator
class order_items(models.Model):
    status = [
        ('Processing', 'processing'),
        ('shipped', 'shipped'),
        ('delivered', 'delivered'),
        ('canceld','canceld')
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
    

class wallet(models.Model):
    user_id=models.ForeignKey(customeUser,on_delete=models.CASCADE,related_name='user_wallet',unique=True)
    wallet_amount=models.DecimalField(max_digits=7,decimal_places=2,)

    def __str__(self):
        return f"{self.user_id.first_name} wallet"

