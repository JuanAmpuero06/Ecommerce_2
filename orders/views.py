from django.shortcuts import render, redirect, get_object_or_404
from transbank.webpay.webpay_plus.transaction import Transaction
from django.conf import settings
from .models import *  # Modelo de órdenes 
from cart.models import *  # Modelo de carrito
from django.contrib.auth.decorators import login_required

@login_required
def iniciar_pago(request):
    cart_items = Cart.objects.filter(user=request.user)  # Obtiene los productos en el carrito
    total = sum(item.product.price * item.quantity for item in cart_items)  # Calcula el total

    if total == 0:  # Evitar pagos con carrito vacío
        return redirect('cart:cart_detail')

    order = Order.objects.create(user=request.user, total=total)  # Crea la orden

    # Agregar los productos del carrito a la orden
    for item in cart_items:
        # Crea una nueva instancia de OrderItem y la guarda
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )

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
    tbk_token = request.GET.get("TBK_TOKEN")
    tbk_order = request.GET.get("TBK_ORDEN_COMPRA")

    # 🔹 CASO 1: El usuario anuló la compra manualmente
    if tbk_token:
        order = get_object_or_404(Order, id=tbk_order)
        order.status = "Anulado"  # ✅ Ahora se marca como "Anulado" en lugar de "Rechazada"
        order.save()
        return redirect("orders:pago_fallido")

    # 🔹 CASO 2: Si no hay `token_ws` ni `TBK_TOKEN`, algo falló
    if not token:
        return redirect("orders:pago_fallido")

    # 🔹 CASO 3: Transacción procesada en Transbank
    transaction = Transaction()
    response = transaction.commit(token)
    response_code = response.get("response_code")


    order = get_object_or_404(Order, id=response.get("buy_order"))

    if response_code == 0:  # Transacción exitosa
        order.status = "Pagado"
        
        # Restar stock de los productos comprados
        for item in order.items.all():
            product = item.product
            product.stock -= item.quantity
            product.save()

        # Vaciar el carrito
        Cart.objects.filter(user=request.user).delete()

        order.save()
        return redirect("orders:pago_exitoso")

    elif response_code and response_code != 0:  # Rechazada después de enviarse a Transbank
        order.status = "Rechazada"
        order.save()
        return redirect("orders:pago_fallido")

    return redirect("orders:pago_fallido")
    
    
    
    
    

def pago_exitoso(request):
    return render(request, "orders/pago_exitoso.html")

def pago_fallido(request):
    return render(request, "orders/pago_fallido.html")