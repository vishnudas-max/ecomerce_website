from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

# Create your models here.
class customer(AbstractUser):
    phoneno=models.BigIntegerField()
    email=models.CharField(max_length=60,unique=True)
    username=models.CharField(max_length=30,unique=True)

    def save(self, *args, **kwargs):
        self.username = self.email
        super().save(*args, **kwargs)

    
    groups = models.ManyToManyField(Group, related_name='customer_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='customer_user_permissions')

    def __str__(self):
        return self.first_name