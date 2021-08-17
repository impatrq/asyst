from django.shortcuts import redirect, render
from django.utils.html import escapejs
from main.models import Stock,Peticion
from django.http import JsonResponse
from django.http.response import JsonResponse
