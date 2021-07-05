from django.shortcuts import render
from main.models import Stock
from django.http import JsonResponse
from django.http.response import JsonResponse
from django.views import View
# Create your views here.
def Home(request):
    return render(request,'login.html')
def Pedir(request):
    stock = Stock.objects.all()
    return render(request,'User-Pedido-Dev(Ped).html')
def Devol(request):
    return render(request,'User-Pedido-Dev(Dev).html')


class StockListView(View):
    def get(self, request):
        sList = Stock.objects.all()
        return JsonResponse(list(sList.values()),safe=False)    


# Borrar esto de abajo y su correspondiente en URLs, es para testear
#def Example(request):
#    return render(request,'scripts/ejemploBase.json')
