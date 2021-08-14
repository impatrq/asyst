from django.urls import path
from .views import *
from django.contrib.auth.views import LoginView,LogoutView

urlpatterns = [path('registrar/',Registrar,name='registrar'),
path('', LoginView.as_view(template_name='login.html',redirect_authenticated_user=True),name='login'),
path('logout/',LogoutView.as_view(template_name='logout.html'),name='logout')]