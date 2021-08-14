from django.shortcuts import render,redirect
from .forms import UserRegisterForm


# Create your views here.
def login(request):
    return render(request,'login.html')

def logout(request):
    return redirect(request,'login')

def Registrar(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # message.sucess(request,f'Usuario {username} creado')
            return redirect('login')
    else:
        form = UserRegisterForm()
    context = {'form':form}
    if not request.user.is_authenticated:
        return render(request,'register.html', context=context)
    else: return redirect('login')