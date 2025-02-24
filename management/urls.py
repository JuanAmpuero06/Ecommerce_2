from django.urls import path
from . import views

app_name = 'management'

urlpatterns = [
    path('productos/', views.product_list, name='product_list'),
    path('productos/agregar/', views.add_product, name='add_product'),
    path('productos/editar/<int:pk>/', views.edit_product, name='edit_product'),
     path('productos/eliminar/<int:product_id>/', views.delete_product, name='delete_product'),
]
