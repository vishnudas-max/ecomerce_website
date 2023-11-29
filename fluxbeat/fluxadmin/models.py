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




class product(models.Model):
    HEADPHONE_TYPES = [
        ('over the Ear', 'Over the Ear'),
        ('on the Ear', 'On the Ear'),
        ('in the Ear', 'In the Ear'),
        ]
    pr_id=models.CharField(max_length=50,null=False,unique=True)
    product_name=models.CharField(max_length=100)
    description=models.TextField(max_length=300)
    product_price=models.IntegerField()
    sale_prce=models.IntegerField()
    total_quantity=models.IntegerField()
    headphone_type = models.CharField(max_length=20, choices=HEADPHONE_TYPES)
    category_id=models.ForeignKey(category,on_delete=models.CASCADE)
    brand_id=models.ForeignKey(brand,on_delete=models.CASCADE)

class images(models.Model):    
    owner=models.CharField(max_length=50)
    image_1=models.ImageField(upload_to='images/')
    
class verients(models.Model):
    varient_color=models.ImageField(upload_to='images/')
    product_id=models.ForeignKey(product,on_delete=models.CASCADE,related_name='product_varients') 
    quantity=models.IntegerField()  
    image_field = models.ManyToManyField(images, related_name='related_images')
