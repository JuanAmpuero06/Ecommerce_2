from django.urls import path
from .views import *

app_name = 'shop'  # Evita conflictos de nombres en otras apps

urlpatterns = [
    path('', home, name='home'),
    path('products/', product_list, name='product_list'),
]