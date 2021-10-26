from django.db import models

# Create your models here.
class Estacion(models.Model):
    nombre = models.CharField(max_length=30)
    ruta = models.CharField(max_length=30)

    def __str__(self):
        return str(self.nombre)+' - '+str(self.ruta)
    
    class Meta: 
        ordering = ['nombre']

class Carrito(models.Model):
    matricula = models.IntegerField()
    rumbo = models.ForeignKey(Estacion,on_delete=models.SET_NULL,null=True,blank=True)
    ocupado = models.BooleanField()
    viajando = models.BooleanField()
    idavuelta = models.BooleanField()
    perdido = models.BooleanField()
    def __str__(self):
        return str(self.matricula)+' - '+str(self.rumbo)
    
    class Meta: 
        ordering = ['matricula']