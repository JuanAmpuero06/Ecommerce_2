from django.db import models
from django.conf import settings
from shop.models import Product

class Order(models.Model):
    STATUS_CHOICES = [
        ('canceled', 'Anulado'),
        ('paid', 'Pagado'),
        ('failed', 'Fallido'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    token = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Orden {self.id} - {self.user.username} - {self.get_status_display()}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Precio unitario

    def total_price(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.quantity}x {self.product.name} en orden {self.order.id}"
    
    def subtotal(self):
        return self.quantity * self.price
