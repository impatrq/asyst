from django.contrib import admin
from .models import Activo, Stock, Peticion
# Register your models here.
admin.site.register(Stock)
admin.site.register(Peticion)
admin.site.register(Activo)