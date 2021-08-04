from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import fields

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField
    password1 = forms.CharField(label='Contraseña',widget=forms.PasswordInput)#(attrs={'class':'input is-medium'}))
    password2 = forms.CharField(label='Comfirmar Contraseña',widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        help_texts = {k:'' for k in fields}