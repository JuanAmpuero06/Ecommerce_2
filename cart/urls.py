from django.urls import path
from .views import *

app_name = 'cart'

urlpatterns = [
    path('', cart_detail, name='cart_detail'),
    path('agregar/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('eliminar/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('disminuir/<int:product_id>/', decrease_quantity, name='decrease_quantity'),
    path('vaciar/', clear_cart, name='clear_cart'),
]
