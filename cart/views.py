from django.shortcuts import render, redirect, get_object_or_404
from shop.models import Product
from .cart import Cart

def cart_detail(request):
    """Muestra los productos en el carrito"""
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})

def add_to_cart(request, product_id):
    """Agrega productos al carrito"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product)
    return redirect('cart:cart_detail')

def remove_from_cart(request, product_id):
    """Elimina un producto del carrito"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

def clear_cart(request):
    """Vacía el carrito"""
    cart = Cart(request)
    cart.clear()
    return redirect('cart:cart_detail')

def decrease_quantity(request, product_id):
    """Disminuye la cantidad de un producto en el carrito"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.decrease(product)
    return redirect('cart:cart_detail')