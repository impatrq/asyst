from django.db import models

# Create your models here.
class Stock(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=22, blank=False, null=False)
    cantidad = models.IntegerField(blank=False, null=False)

    class Clase(models.IntegerChoices):
        INSUMO = 1
        HERRAMIENTA = 2
    clase = models.IntegerField(choices=Clase.choices)

    def __str__(self):
        return self.nombre
    
    class Meta:
        ordering = ['nombre']
