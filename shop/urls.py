from django.urls import path
from .views import home

app_name = 'shop'  # Evita conflictos de nombres en otras apps

urlpatterns = [
    path('', home, name='home'),
]