from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import CustomUserCreationForm


# Create your views here.

def register(request):
    formulario_usuario = CustomUserCreationForm()
    if request.method == 'POST':
        formulario_usuario=CustomUserCreationForm(request.POST)
        if formulario_usuario.is_valid():
            formulario_usuario.save()
            usuario = authenticate(username=formulario_usuario.cleaned_data['username'], password=formulario_usuario.cleaned_data['password1'])
            # messages.add_message(request, messages.SUCCESS, 'Bienvenido', extra_tags='success')
            print(f'usuario: {usuario}')
            login(request, usuario)
    contexto = {
        'form': formulario_usuario,
    }

    
    return render(request, 'registration/register.html', contexto)