from django.urls import path
from . import views

urlpatterns = [
   
    path('', views.gestion, name='Gestion'),
    path('establecer_stock/', views.establecer_stock, name='establecerStock'),
    path('obtener_pedido/', views.obtener_pedido, name='obtener_pedido'),
    path('actualizar_pedido/', views.actualizar_pedido, name='actualizar_pedido'),
    path('comprobar_nuevos_pedidos/', views.comprobar_nuevos_pedidos, name='obtener_pedidos'),
]