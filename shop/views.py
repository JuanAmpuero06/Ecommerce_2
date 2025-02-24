from django.shortcuts import render
from .models import *

def home(request):
    return render(request, 'home.html')

def product_list(request):
    """Muestra todos los productos disponibles en la tienda"""
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})