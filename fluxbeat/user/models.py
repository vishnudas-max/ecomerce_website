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