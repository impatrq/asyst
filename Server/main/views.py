from django.shortcuts import redirect, render
from django.utils.html import escapejs
from main.models import Stock
from django.http import JsonResponse
from django.http.response import JsonResponse
from django.views import View
from .forms import UserRegisterForm
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


def Registrar(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        print('1')
        if form.is_valid():
            form.save()
            # message.sucess(request,f'Usuario {username} creado')
            print('2')
            return redirect('login')
    else:
        form = UserRegisterForm()
        print('3')
    context = {'form':form}
    return render(request,'register.html', context=context)

def login2(request):
    return render(request,'login.html')

def logout(request):
    return redirect(request,'login2')


# Borrar esto de abajo y su correspondiente en URLs, es para testear
#def Example(request):
#    return render(request,'scripts/ejemploBase.json')
