from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.http.response import JsonResponse, HttpResponse
from django.forms.models import model_to_dict
import json
from .models import *
# Create your views here.
@csrf_exempt
def carrito(request):
    if request.method == 'GET':
        if request.GET.get('matricula'):
            if request.GET.get('matricula') == '0':
                return JsonResponse(list(Carrito.objects.all().values()), safe=False)
            encontrado = False
            for carrito in Carrito.objects.all():
                if int(carrito.matricula) == int(request.GET.get('matricula')):
                    encontrado = True
            if not encontrado:
                return HttpResponse('ERROR, matricula invalida')

            matricula = request.GET.get('matricula')
            carr = Carrito.objects.get(matricula=matricula)
            carritodata = model_to_dict(carr)
            try:
                carritodata['rumbo'] = carr.rumbo.ruta
            except:pass
            return JsonResponse(carritodata,safe=False)

        else:
            return HttpResponse('ERROR, ingrese matricula')

    if request.method == 'POST':
        print(request.body.decode('utf-8'))
        return redirect('carrito')
