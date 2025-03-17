from django.urls import path
from . import views
from .views import *

app_name = 'orders'

urlpatterns = [
    path('pago/', iniciar_pago, name='iniciar_pago'),
    path('confirmacion/', confirmacion_pago, name='confirmacion_pago'),
    path("pago/exitoso/", views.pago_exitoso, name="pago_exitoso"),
    path("pago/fallido/", views.pago_fallido, name="pago_fallido"),
    path('mis-ordenes/', lista_ordenes, name='lista_ordenes'),
    path('orden/<int:order_id>/', detalle_orden, name='detalle_orden'),
]
