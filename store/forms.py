from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'price', 'stock', 'image', 'description']

        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
        }


