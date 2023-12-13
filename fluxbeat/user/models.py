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
    address_type=models.CharField(max_length=100,null=False)

    def __str__(self):
        return "Address of {first_named}"