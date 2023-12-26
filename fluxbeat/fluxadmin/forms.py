from django import forms
from .models import brand,category,images,coupon
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.utils.timezone import now
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

class couponform(forms.ModelForm):
    exp_date = forms.DateField(
        widget=forms.TextInput(attrs={'type': 'date'}),
        validators=[MinValueValidator(now().date())]  # Restrict to dates from today onwards
    )

    class Meta:
        model = coupon
        fields = ("coupon_name", "code", "min_amount", "offer_per", "exp_date")
    def clean_code(self):
        code = self.cleaned_data['code']
        if not code.isalnum() or not any(char.isalpha() for char in code) or not any(char.isdigit() for char in code):
            raise forms.ValidationError("Code must be a mix of numbers and capital letters.")
        return code

    def clean(self):
        cleaned_data = super().clean()
        min_amount = cleaned_data.get('min_amount')
        offer_per = cleaned_data.get('offer_per')

        # Additional validation logic for min_amount and offer_per if needed

        return cleaned_data
    def clean_code(self):
        code = self.cleaned_data['code']

        # Check if a coupon with the same code already exists
        existing_coupon = coupon.objects.filter(code=code).exclude(pk=self.instance.pk).first()

        if existing_coupon:
            raise forms.ValidationError("A coupon with this code already exists.")

        if not code.isalnum() or not any(char.isalpha() for char in code) or not any(char.isdigit() for char in code):
            raise forms.ValidationError("Code must be a mix of numbers and capital letters.")

        return code

    
