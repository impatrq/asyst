from django.shortcuts import redirect, render
from django.utils.html import escapejs
from main.models import Stock,Peticion
from django.http import JsonResponse
from django.http.response import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
import json

@staff_member_required(login_url='home')
def staffHome(request):
    return redirect('pedidos')

# ------------------------------------------------------- PEDIDOS -----------------------------------
@staff_member_required(login_url='home')
def pedidos(request):
    pendientes = Peticion.objects.filter(estado = 1)
    return render(request,'Staff-pedidos.html',context={'pendientes':pendientes})


#--------------------------------------------STOCK---------------------------------------------------
@staff_member_required(login_url='home')
def stock(request):
    if request.method =='GET':
        stockDb = Stock.objects.all()
        stock = JsonResponse(list(stockDb.values()),safe=False)
        for i in stock: stock = i.decode('utf-8')
        return render(request,'Staff-stock.html',context={'stock':stock})

@staff_member_required(login_url='home')
def addStock(request):
    if request.method == 'POST':
        # print(request.body)
        req = json.loads(request.body.decode('utf-8'))
        print(req)
        stock = Stock(
            nombre= req['nombre'],
            cantidad= req['cantidad'],
            clase= req['clase']
        )
        stock.save()
    return redirect('stock')

@staff_member_required(login_url='home')
def editStock(request,id):
    if request.method == 'POST':
        # print(request.body)
        req = json.loads(request.body.decode('utf-8'))
        edited = Stock.objects.get(id=id)
        print(req)
        edited.nombre = req['nombre']
        edited.clase = req['clase']
        edited.cantidad = req['cantidad']
        edited.save()
    return redirect('stock')

@staff_member_required
def removeStock(request, id):
    dato = Stock.objects.get(id=id)
    dato.delete()
    return redirect('stock')

# ----------------------------------------------------REGISTROS------------------------------------
@staff_member_required(login_url='home')
def registros(request):
    peticiones = Peticion.objects.exclude(estado=1)
    return render(request,'Staff-registros.html',context={'peticiones':peticiones})
