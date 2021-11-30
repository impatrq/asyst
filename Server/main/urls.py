from django.urls import path
from .views import *
from django.contrib.auth.views import LoginView,LogoutView
urlpatterns = [
    # path('',Home, name='login'),
    path('pedir/',Pedir, name='pedir'),
    path('devolver/',Devol, name='devol'),
    #path('stocklist/',ReadStock, name='stocklist'),
    # Borrar el Path de abajo y su correspondiente en views, es para testear
    #path('pedir/scripts/ejemploBase.json',Example, name='example'),
    # path('getstock/',StockListView.as_view()),
    path('data/',userData,name='userData'),
    path('devolver/<int:id>/',segEstado)
]    