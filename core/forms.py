from django import forms
from .models import Product, DetectionRun
from decimal import Decimal


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'sku', 'category', 'unit_price', 'stock', 'weekly_sales_estimate', 'profit_margin']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'sku': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'weekly_sales_estimate': forms.NumberInput(attrs={'class': 'form-control'}),
            'profit_margin': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '1'}),
        }


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = DetectionRun
        fields = ['uploaded_image']
        widgets = {
            'uploaded_image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }

