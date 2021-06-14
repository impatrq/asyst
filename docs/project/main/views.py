from django.shortcuts import render
from django.http import HttpResponse
login = open('/hola.html')
# Create your views here.
def homepage(request):
    return HttpResponse(login)