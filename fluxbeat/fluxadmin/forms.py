from django import forms
from .models import brand,category,images
from django.core.exceptions import ValidationError
class ImageForm(forms.ModelForm):
    class Meta:
        model = brand
        fields = ("brand_name", "brand_image")


class CategoryForm(forms.ModelForm):
    class Meta:
        model = category
        fields =('category_name',)
    def clean_category_name(self):
        category_name=self.cleaned_data.get('category_name')

        if category.objects.filter(category_name__iexact=category_name).exists():
            raise ValidationError('Category with this name already excists !')
        return category_name
    
