from django import forms
from .models import brand,category,images
class ImageForm(forms.ModelForm):
    class Meta:
        model = brand
        fields = ("brand_name", "brand_image")


class CategoryForm(forms.ModelForm):
    class Meta:
        model = category
        fields =('category_name',)
