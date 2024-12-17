from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from .models import Trabajador, Departamento, Area, CargaFamiliar
from .forms import TrabajadorForm, CargaFamiliarForm, DepartamentoForm, AreaForm
from .decorators import trabajador_login_required
from django.contrib.auth.models import User
from django.db.models import Q


def listar_trabajador(request):
    busqueda = request.POST.get("buscar")  
    trabajadores = Trabajador.objects.all()

    if busqueda:
        trabajadores = trabajadores.filter(
            Q(rut__icontains=busqueda) | 
            Q(nombre__icontains=busqueda) |  
            Q(apellido__icontains=busqueda) | 
            Q(departamento__icontains=busqueda) |  
            Q(area__icontains=busqueda)  
        ).distinct()  

    return render(request, 'trabajador_list.html', {'trabajadores': trabajadores})

@login_required
def trabajador_list(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("No tienes permiso para ver esta página.")
    
    busqueda = request.POST.get("buscar")  

 
    trabajadores = Trabajador.objects.all()


    if busqueda:
        trabajadores = trabajadores.filter(
            Q(rut__icontains=busqueda) |  # Filtrar por rut
            Q(nombre__icontains=busqueda) |  # Filtrar por nombre
            Q(apellido__icontains=busqueda)   # Filtrar por apellido
             
        ).distinct()  
    
   
    return render(request, 'trabajador/list.html', {'trabajadores': trabajadores})



def trabajador_detail(request, pk):
    trabajador = Trabajador.objects.get(pk=pk)
    return render(request, 'trabajador/detail.html', {'trabajador': trabajador})


def trabajador_create(request):
    if request.method == 'POST':
       
        trabajador_form = TrabajadorForm(request.POST)
        

       
        if trabajador_form.is_valid():
            
            trabajador = trabajador_form.save(commit=False)
            username = trabajador_form.cleaned_data['rut']
            password = request.POST.get('password', 'defaultpassword')  
            user = User.objects.create_user(username=username, password=password)

            trabajador.user = user
            trabajador.save()

            return redirect('trabajador-list')
    else:
        trabajador_form = TrabajadorForm()
        

    
    return render(request, 'trabajador/form.html', {
        'trabajador_form': trabajador_form,
        
        'title': 'Crear Trabajador'
    })





def trabajador_update(request, pk):
    trabajador = get_object_or_404(Trabajador, pk=pk)
    print(trabajador)  

    if request.method == 'POST':
        trabajador_form = TrabajadorForm(request.POST, instance=trabajador)
        if trabajador_form.is_valid():
            trabajador_form.save()
            return redirect('trabajador-list')
    else:
        trabajador_form = TrabajadorForm(instance=trabajador)

    return render(request, 'trabajador/editar_trabajador.html', {
        'trabajador_form': trabajador_form,
        'title': 'Editar Trabajador'
    })





def trabajador_delete(request, pk):
    trabajador = get_object_or_404(Trabajador, pk=pk)
    user = trabajador.user

    if request.method == 'POST':
        user.delete()
        trabajador.delete()
        
        return redirect('trabajador-list')
    
    return render(request, 'trabajador/confirm_delete.html', {'trabajador': trabajador})


def carga_familiar_create(request):
    if request.method == 'POST':
        form = CargaFamiliarForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('trabajador-list')
    else:
        form = CargaFamiliarForm()
    return render(request, 'trabajador/carga_familiar_form.html', {'form': form})

def carga_familiar_update(request, pk):
    carga_familiar = get_object_or_404(CargaFamiliar, pk=pk)
    if request.method == 'POST':
        form = CargaFamiliarForm(request.POST, instance=carga_familiar)
        if form.is_valid():
            form.save()
            return redirect('trabajador-list')
    else:
        form = CargaFamiliarForm(instance=carga_familiar)
    return render(request, 'trabajador/carga_familiar_form.html', {'form': form})

