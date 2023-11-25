from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

# Create your models here.
class customer(AbstractUser):
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    phoneno=models.BigIntegerField()
    email=models.CharField(max_length=60,unique=True)
    password=models.CharField(max_length=80)
    is_superuser=models.BooleanField(default=False)
    username=models.CharField(max_length=50,blank=True,unique=False)

    
    groups = models.ManyToManyField(Group, related_name='customer_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='customer_user_permissions')

    def __str__(self):
        return self.first_name