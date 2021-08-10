from django.shortcuts import redirect, render
from django.utils.html import escapejs
from main.models import Stock
from django.http import JsonResponse
from django.http.response import JsonResponse
from django.views import View
from .forms import UserRegisterForm
# Create your views here.
def Pedir(request):
    stock = Stock.objects.all()
    print(request.user.username)
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('/admin')
        return render(request,'User-Pedido-Dev(Ped).html')
    else: return redirect('login')
def Devol(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('/admin')
        return render(request,'User-Pedido-Dev(Dev).html')
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
