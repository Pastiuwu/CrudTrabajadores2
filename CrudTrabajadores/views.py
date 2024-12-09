from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from .models import Trabajador, Departamento, Area, CargaFamiliar
from .forms import TrabajadorForm, CargaFamiliarForm, DepartamentoForm, AreaForm
from .decorators import trabajador_login_required
from django.contrib.auth.models import User
from django.db.models import Q


def listar_trabajador(request):
    busqueda = request.POST.get("buscar")  # Cambio aquí: se usa POST porque el formulario usa POST
    trabajadores = Trabajador.objects.all()

    if busqueda:
        trabajadores = trabajadores.filter(
            Q(rut__icontains=busqueda) |  # Cambié "rut_icontains" por "rut__icontains"
            Q(nombre__icontains=busqueda) |  # Cambié "nombre_icontains" por "nombre__icontains"
            Q(apellido__icontains=busqueda) |  # Cambié "apellido" por "apellido__icontains"
            Q(departamento__icontains=busqueda) |  # Cambié "departamento" por "departamento__icontains"
            Q(area__icontains=busqueda)  # Cambié "area_icontains" por "area__icontains"
        ).distinct()  # Arreglé el typo en .distinct()

    return render(request, 'trabajador_list.html', {'trabajadores': trabajadores})

@login_required
def trabajador_list(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("No tienes permiso para ver esta página.")
    
    # Obtener la búsqueda desde el formulario
    busqueda = request.POST.get("buscar")  # Usamos POST para obtener la búsqueda

    # Obtener todos los trabajadores
    trabajadores = Trabajador.objects.all()

    # Si hay algo en el campo de búsqueda, filtramos los trabajadores
    if busqueda:
        trabajadores = trabajadores.filter(
            Q(rut__icontains=busqueda) |  # Filtrar por rut
            Q(nombre__icontains=busqueda) |  # Filtrar por nombre
            Q(apellido__icontains=busqueda)   # Filtrar por apellido
             # Filtrar por nombre de área
        ).distinct()  # Eliminar duplicados
    
    # Renderizar la plantilla con los trabajadores filtrados (o todos si no hay búsqueda)
    return render(request, 'trabajador/list.html', {'trabajadores': trabajadores})



def trabajador_detail(request, pk):
    trabajador = Trabajador.objects.get(pk=pk)
    return render(request, 'trabajador/detail.html', {'trabajador': trabajador})


def trabajador_create(request):
    if request.method == 'POST':
        # Crear ambos formularios
        trabajador_form = TrabajadorForm(request.POST)
        

        # Verificar que ambos formularios sean válidos
        if trabajador_form.is_valid():
            # Crear el trabajador, pero no guardarlo aún
            trabajador = trabajador_form.save(commit=False)

            # Crear un usuario asociado al trabajador usando el RUT como username
            username = trabajador_form.cleaned_data['rut']
            password = request.POST.get('password', 'defaultpassword')  # Contraseña por defecto
            user = User.objects.create_user(username=username, password=password)

            # Asignar el usuario al trabajador y guardar
            trabajador.user = user
            trabajador.save()

            

            # Redirigir al listado de trabajadores
            return redirect('trabajador-list')
    else:
        # Inicializar los formularios vacíos
        trabajador_form = TrabajadorForm()
        

    # Pasar los formularios a la plantilla
    return render(request, 'trabajador/form.html', {
        'trabajador_form': trabajador_form,
        
        'title': 'Crear Trabajador'
    })





def trabajador_update(request, pk):
    trabajador = get_object_or_404(Trabajador, pk=pk)
    print(trabajador)  # Verifica que el trabajador tiene datos

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
    
    # Obtener el usuario asociado al trabajador
    user = trabajador.user

    if request.method == 'POST':
        # Eliminar primero el usuario
        user.delete()
        
        # Luego eliminar el trabajador
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

