from decimal import Decimal
from django.conf import settings
from shop.models import Product

class Cart:
    def __init__(self, request):
        """Inicializa el carrito"""
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, quantity=1):
        """Agrega productos al carrito"""
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        
        self.cart[product_id]['quantity'] += quantity
        self.save()

    def decrease(self, product):
        """Reduce la cantidad de un producto en el carrito"""
        product_id = str(product.id)
        if product_id in self.cart:
            if self.cart[product_id]['quantity'] > 1:
                self.cart[product_id]['quantity'] -= 1
            else:
                del self.cart[product_id]  # Elimina el producto si la cantidad es 0
            self.save()

    def save(self):
        """Guarda los cambios en la sesión"""
        self.session.modified = True

    def remove(self, product):
        """Elimina un producto del carrito completamente"""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """Itera sobre los productos en el carrito"""
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """Cuenta la cantidad total de productos en el carrito"""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """Calcula el precio total del carrito"""
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """Vacía el carrito"""
        del self.session['cart']
        self.save()
