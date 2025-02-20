from django.urls import path
from . import views

urlpatterns = [
   
    path('', views.zonas, name='Zonas'),
    path('form_zonas/', views.form_zonas, name='NuevaZona'),
    path('update_zon/<int:pk>/', views.update_zon, name='update_zon'),
    path('delete_zon/<int:pk>/', views.delete_zon, name='delete_zon')
]