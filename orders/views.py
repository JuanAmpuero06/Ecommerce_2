from django.shortcuts import render, redirect, get_object_or_404
from transbank.webpay.webpay_plus.transaction import Transaction
from django.conf import settings
from .models import Order  # Modelo de órdenes 
from cart.models import Cart  # Modelo de carrito
from django.contrib.auth.decorators import login_required

@login_required
def iniciar_pago(request):
    cart_items = Cart.objects.filter(user=request.user)  # Obtiene los productos en el carrito
    total = sum(item.product.price * item.quantity for item in cart_items)  # Calcula el total

    if total == 0:  # Evitar pagos con carrito vacío
        return redirect('cart:cart_detail')

    order = Order.objects.create(user=request.user, total=total)  # Crea la orden

    tx = Transaction()
    response = tx.create(
        buy_order=str(order.id),
        session_id=str(request.user.id),
        amount=float(total),
        return_url=settings.TRANSBANK_RETURN_URL
    )

    order.token = response['token']  # Guarda el token de la transacción
    order.save()

    return redirect(response['url'] + '?token_ws=' + response['token'])

def confirmacion_pago(request):
    token = request.GET.get("token_ws")

    if not token:
        return redirect("orders:pago_fallido")

    transaction = Transaction()
    response = transaction.commit(token)

    if response.get("response_code") == 0:  # Código 0 indica transacción exitosa
        order = get_object_or_404(Order, id=response.get("buy_order"))

        # 🔹 Restar stock de los productos comprados
        for item in order.items.all():
            product = item.product
            product.stock -= item.quantity
            product.save()

        # 🔹 Marcar la orden como pagada
        order.status = "Pagado"
        order.save()

        # 🔹 Vaciar el carrito del usuario
        cart = Cart.objects.filter(user=request.user)
        cart.delete()  # Elimina todos los productos del carrito

        return redirect("orders:pago_exitoso")
    else:
        return redirect("orders:pago_fallido")
    
    
    
    
    

def pago_exitoso(request):
    return render(request, "orders/pago_exitoso.html")

def pago_fallido(request):
    return render(request, "orders/pago_fallido.html")