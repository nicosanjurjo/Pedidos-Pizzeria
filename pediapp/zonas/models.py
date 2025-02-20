from django.db import models

class Zona(models.Model):
    nombre_zona = models.CharField(max_length=50)
    descripcion_zona = models.CharField(max_length=100)
    costo = models.IntegerField()
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre_zona}"