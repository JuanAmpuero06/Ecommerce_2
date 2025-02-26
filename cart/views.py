from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from shop.models import Product
from .models import Cart

@login_required
def cart_detail(request):
    """Muestra los productos en el carrito"""
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.total_price() for item in cart_items)  # Total del carrito
    return render(request, 'cart/cart_detail.html', {'cart_items': cart_items, 'total': total})

@login_required
def add_to_cart(request, product_id):
    """Agrega un producto al carrito"""
    product = get_object_or_404(Product, id=product_id)

    # Busca si el producto ya está en el carrito del usuario
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart:cart_detail')

@login_required
def remove_from_cart(request, product_id):
    """Reduce la cantidad de un producto o lo elimina si la cantidad es 1"""
    cart_item = Cart.objects.filter(user=request.user, product_id=product_id).first()
    
    if cart_item:
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

    return redirect('cart:cart_detail')

@login_required
def clear_cart(request):
    """Vacía completamente el carrito"""
    Cart.objects.filter(user=request.user).delete()
    return redirect('cart:cart_detail')
