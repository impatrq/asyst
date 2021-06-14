from django.urls import path, include
from django.urls.resolvers import URLPattern
from . import views

app_name = 'main'
urlpatterns = [
    path('', views.homepage, name="homepage")
]