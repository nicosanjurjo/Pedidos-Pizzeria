from django.db import models

class Estado(models.Model):
    estado= models.BooleanField()
    pedidosdespachados = models.SmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)