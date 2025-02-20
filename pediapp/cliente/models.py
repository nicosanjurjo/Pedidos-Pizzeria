from django.db import models
from zonas.models import Zona

class Turno(models.Model):
    horario = models.TimeField()
    max_pedidos = models.IntegerField(default=10)
    pedidos_actuales = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.horario}"

    def disponible(self):
        return self.pedidos_actuales < self.max_pedidos

class Pedido(models.Model):

    PAGO_CHOICES = [
        ('Efectivo', 'Efectivo'),
        ('Transferencia/MP', 'Transferencia/MP')
    ]

    ENTREGA_CHOICES = [
        ('Retiro', 'Retiro por local'),
        ('Envio', 'Envio a domicilio')
    ]

    nombre = models.CharField(max_length=25)
    telefono = models.CharField(max_length=20)
    detalles = models.TextField()  # Este campo almacenará los detalles del pedido en formato JSON o texto plano.
    monto = models.IntegerField()
    estado = models.CharField(max_length=15, default='Tomado')
    horario = models.CharField(max_length=5, null=True, blank=True)
    medio_pago = models.CharField(max_length=25, choices=PAGO_CHOICES, default='Efectivo')
    metodo_entrega = models.CharField(max_length=25, choices=ENTREGA_CHOICES, default='Retiro en local')
    direccion = models.CharField(max_length=200, blank=True, null=True)
    observaciones = models.TextField(max_length=150, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    visto=models.BooleanField(default=False)

    def __str__(self):
        return f"Pedido #{self.id} - {self.nombre}"
