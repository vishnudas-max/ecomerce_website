from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
User=get_user_model()
from django.core.validators import MinValueValidator
# Create your models here.
class brand(models.Model):
    brand_name=models.CharField(max_length=40,unique=True,null=False)
    brand_image=models.ImageField(upload_to='images/')
    is_active=models.BooleanField(default=True)
    brand_date=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.brand_name
    
class category(models.Model):
    category_name=models.CharField(max_length=50,unique=True,null=False,)
    is_active=models.BooleanField(default=True,blank=True)
    cat_date=models.DateField(auto_now_add=True)

class special_offer(models.Model):
    offer_title=models.CharField(max_length=200,unique=True,null=False)
    banner_image=models.ImageField(upload_to='images/')
    stat_date=models.DateField()
    end_date=models.DateField()
    offer_per=models.IntegerField(null=False,)
    appied_for=models.CharField(max_length=100)
    namee=models.CharField(max_length=100)

    def __str__(self):
        return self.offer_title

class product(models.Model):
    HEADPHONE_TYPES = [
        ('over the Ear', 'Over the Ear'),
        ('on the Ear', 'On the Ear'),
        ('in the Ear', 'In the Ear'),
        ]
    pr_id=models.CharField(max_length=50,null=False,unique=True)
    product_name=models.CharField(max_length=300)
    description=models.TextField(max_length=500)
    product_price=models.IntegerField()
    sale_prce=models.IntegerField()
    total_quantity=models.IntegerField()
    headphone_type = models.CharField(max_length=20, choices=HEADPHONE_TYPES)
    category_id=models.ForeignKey(category,on_delete=models.CASCADE,related_name='category_products')
    brand_id=models.ForeignKey(brand,on_delete=models.CASCADE)
    is_active=models.BooleanField(default=True)
    product_image=models.ImageField(upload_to='images/')
    product_date=models.DateField(auto_now_add=True)
    offer_applied=models.ForeignKey(special_offer,on_delete=models.CASCADE,related_name='offer_applied_products',null=True)
    offer_amount=models.DecimalField(max_digits=10,decimal_places=2,null=True)
   

class images(models.Model):    
    owner=models.CharField(max_length=50)
    image_1=models.ImageField(upload_to='images/')
    
    
class verients(models.Model):
    varient_id=models.CharField(max_length=50,null=False,unique=True)
    varient_color=models.ImageField(upload_to='images/')
    product_id=models.ForeignKey(product,on_delete=models.CASCADE,related_name='product_varients') 
    quantity=models.IntegerField()  
    image_field = models.ManyToManyField(images, related_name='related_images')
    varient_date=models.DateField(auto_now_add=True)

class cart(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.CASCADE,related_name='cart_items',null=False)
    proudct_id=models.ForeignKey(product,on_delete=models.CASCADE,related_name='cart_items',null=False)
    varient_id=models.ForeignKey(verients,on_delete=models.CASCADE,null=False)
    proudct_quantity=models.IntegerField(validators=[MinValueValidator(0)],
        help_text='Enter a positive integer for product quantity',default=1)
    added_date=models.DateField(auto_now_add=True)
    total_price=models.DecimalField(max_digits=10, decimal_places=2,blank=True)

    def save(self, *args, **kwargs):
        # Calculate total_price before saving
        self.total_price = self.proudct_quantity * self.proudct_id.sale_prce
        super().save(*args, **kwargs)
        
class coupon(models.Model):
    coupon_name=models.CharField(max_length=50,null=False,unique=True)
    code=models.CharField(max_length=50,null=False,unique=True)
    min_amount=models.DecimalField(max_digits=10,decimal_places=2)
    offer_per=models.DecimalField(max_digits=2,decimal_places=0)
    starting_date=models.DateField(auto_now_add=True)
    exp_date=models.DateField(null=False)

    def __str__(self):
        return self.coupon_name


