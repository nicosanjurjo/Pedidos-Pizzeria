from django.urls import path
from . import views

urlpatterns = [
   
    path('', views.cliente, name='Cliente'),
    path('form_cliente/', views.clienteform, name='Clienteform'),
    path('form_cliente/confirmado/', views.crear_pedido, name='crear_pedido'),
    path('pedido/<str:telefono>/', views.pedido, name='detalle_pedido'),
]