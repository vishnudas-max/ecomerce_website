from django.db import models

# Create your models here.
class brand(models.Model):
    brand_name=models.CharField(max_length=40,unique=True,null=False)
    brand_image=models.ImageField(upload_to='images/')
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.brand_name
    
class category(models.Model):
    category_name=models.CharField(max_length=50,unique=True,null=False,)
    is_active=models.BooleanField(default=True,blank=True)

class verients(models.Model):
    varient_color=models.CharField(max_length=50)
    color_images=                                                                     