from django.db import models
from django.contrib.auth.models import User
from carrito.models import Carrito, Estacion

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

class Peticion(models.Model):
    id = models.AutoField(primary_key=True)
    autor =  models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    hora = models.DateTimeField(auto_now_add=True)
    class Estado(models.IntegerChoices):
        PENDIENTE = 1
        APROBADA  = 2
        RECHAZADA = 3
        ACTIVA    = 4
    estado = models.IntegerField(choices=Estado.choices)
    pedido = models.TextField(null=True)
    mensaje = models.TextField(default=None, blank=True, null=True)
    staff =  models.ForeignKey(User,on_delete=models.SET_NULL,default=None, blank=True, null=True,related_name='staff_a_cargo')
    destino = models.ForeignKey(Estacion,on_delete=models.SET_NULL,default=None,blank=True,null=True,related_name='destino')

    def __str__(self):
        return str(self.autor) +" - "+ str(self.Estado.choices[self.estado-1][1]) #+" - "+ str(self.hora)

    class Meta:
        ordering = ['hora']

class Activo(models.Model):
    usuario = models.OneToOneField(User,on_delete=models.SET_NULL,default=None, blank=True, null=True)
    pedido = models.OneToOneField(Peticion,on_delete=models.SET_NULL,default=None, blank=True, null=True)
    carrito = models.ForeignKey(Carrito,on_delete=models.SET_NULL,default=None, blank=True, null=True)
    def __str__(self) -> str:
        return str(self.usuario) + ' - ' + str(self.carrito) 