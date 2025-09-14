# inventario/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.galeria_productos, name='galeria_productos'),
    path('agregar/', views.agregar_producto, name='agregar_producto'),
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('vender/<int:producto_id>/', views.registrar_venta, name='registrar_venta'),
    path('historial/', views.historial_ventas, name='historial_ventas'),
]