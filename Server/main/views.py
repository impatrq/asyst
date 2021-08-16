from django.shortcuts import redirect, render
from django.utils.html import escapejs
from main.models import Stock,Peticion
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
        print('-')
    print(stock)
    print(request.user.username)
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('/admin')

        if request.method=='POST': # Si hago un POST (desde el boton de enviar)
            # print(request.POST)
            # print(request.body.decode('utf-8')) # convierto los bytes a string
            lista = json.loads(request.body.decode('utf-8')) # lo cargo como json
            for i in lista:                                 # lo muestro en consola
                print(i + '-'*15)
                for j in lista[i]:
                    print (str(j) + '= '+ str(lista[i][j]))
            peticion = Peticion(                            # creo una peticion y la envio
                autor=request.user,
                estado=1,
                pedido=request.body.decode('utf-8'))
            peticion.save()

        return render(request,'User-Pedido-Dev(Ped).html',context={"stock":stock})
    else: return redirect('login')

def Devol(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('/admin')
        pedido = Peticion.objects.filter(estado=1,autor= request.user)
        print(pedido)
        return render(request,'User-Pedido-Dev(Dev).html',context={'pedido':pedido[0]})
    else: return redirect('login')


class StockListView(View):
    def get(self, request):
        sList = Stock.objects.all()
        return JsonResponse(list(sList.values()),safe=False)    


def home(request):
    return redirect('login')
# Borrar esto de abajo y su correspondiente en URLs, es para testear
#def Example(request):
#    return render(request,'scripts/ejemploBase.json')
