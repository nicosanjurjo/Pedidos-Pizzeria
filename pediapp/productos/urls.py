from django.urls import path
from . import views

urlpatterns = [
   
    path('', views.productos, name='Productos'),
    path('form_productos/', views.form_productos, name='NuevoProducto'),
    path('update_pro/<int:pk>/', views.update_pro, name='update_pro'),
    path('delete_pro/<int:pk>/', views.delete_pro, name='delete_pro')
]