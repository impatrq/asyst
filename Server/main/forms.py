from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import fields

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'class':'input is-medium','placeholder':'Usuario'}))
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={'class':'input is-medium','placeholder':'Email'}),
        required=False)
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class':'input is-medium','placeholder':'Contraseña'}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class':'input is-medium','placeholder':'Confirmar Contraseña'}))
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class':'input is-medium','placeholder':'Nombre'}),
        required=False)
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class':'input is-medium','placeholder':'Apellido'}),
        required=False)
    is_staff = forms.BooleanField()

    class Meta:
        model = User
        fields = ['username','email','password1','password2','first_name','last_name','is_staff']
        help_texts = {k:'' for k in fields}