from django.urls import path
from .views import *
urlpatterns = [
    # path('',Home, name='login'),
    path('pedidos/',pedidos,name='pedidos'),
    path('stock/',stock,name='stock'),
    path('registros/',registros,name='registros'),
    path('stock/add/',addStock,name='addStock'),
    path('stock/remove/<int:id>/',removeStock,name='removeStock'),
    path('stock/edit/<int:id>/',editStock,name='editStock'),
    path('',staffHome,name='staffHome')
]    