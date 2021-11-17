from django.shortcuts import redirect, render
from django.utils.html import escapejs
from main.models import Stock,Peticion, Activo
from carrito.models import Estacion
from django.http import JsonResponse
from django.http.response import JsonResponse
from django.views import View
from .forms import UserRegisterForm
from django.core import serializers
import json
# Create your views here.
def Pedir(request):
    stockDb = Stock.objects.all()
    stock = JsonResponse(list(stockDb.values()),safe=False)
    for i in stock:
        print(i)
        stock = i.decode('utf-8')
        print('-')
    print('-------------------')
    estacionesDb = Estacion.objects.all()
    estaciones = JsonResponse(list(estacionesDb.values()),safe=False)
    for i in estaciones:
        print(i)
        estaciones = i.decode('utf-8')
        print('-')
    print(stock)
    print(request.user.username)
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('/staff')

        if request.method=='POST': # Si hago un POST (desde el boton de enviar)
            # print(request.POST)
            # print(request.body.decode('utf-8')) # convierto los bytes a string
            lista = json.loads(request.body.decode('utf-8')) # lo cargo como json
            print(lista)
            data = request.body.decode('utf-8')
            lugar = lista[0]
            lista.pop(0)
            peticion = Peticion(                            # creo una peticion y la envio
                autor=request.user,
                estado=1,
                pedido=str(lista).replace('\'','"'),
                destino = Estacion.objects.get(id=lugar))
            activo = Activo.objects.get(usuario=request.user)
            activo.pedido = peticion
            activo.carrito = None
            peticion.save()
            activo.save()

        return render(request,'User-Pedido-Dev(Ped).html',context={"stock":stock,"estaciones":estaciones})
    else: return redirect('login')

def Devol(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('/admin')
        activo = Activo.objects.get(usuario=request.user)
        estado = 0
        if activo.pedido.estado == 2:
            estado = 1
            if activo.carrito.viajando == True:
                estado = 2
                if activo.carrito.idavuelta == True:
                    estado = 3
        elif activo.pedido.estado == 3:
            estado = 4
        
        print(activo.pedido)
        pedido2 = activo.pedido
        # print(f'{estado}:{activo.carrito.matricula}')

        if request.method == 'POST':
            pedido2.mensaje = request.body.decode('utf-8')
            print(request.body.decode('utf-8'))
            pedido2.save()
        # print(pedido)
        return render(request,'User-Pedido-Dev(Dev).html',context={'pedido':pedido2,'estado':estado})
    else: return redirect('login')




def home(request):
    return redirect('login')
# Borrar esto de abajo y su correspondiente en URLs, es para testear
#def Example(request):
#    return render(request,'scripts/ejemploBase.json')
def userData(request):
    peticiones = Peticion.objects.filter(autor = request.user)
    return render(request,'User-data.html',context={'peticiones':peticiones})
