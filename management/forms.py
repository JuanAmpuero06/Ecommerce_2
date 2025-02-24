# management/forms.py
from django import forms
from shop.models import *

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock', 'image', 'category']

    # Opcional: Agregar un widget para mostrar las categorías
    category = forms.ModelChoiceField(queryset=Category.objects.all())
