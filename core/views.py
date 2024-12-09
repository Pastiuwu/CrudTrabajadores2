from django.shortcuts import render, redirect
from django.http import HttpResponse
from CrudTrabajadores.models import Trabajador
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from CrudTrabajadores.forms import RegistroTrabajadorForm
from django.contrib.auth import logout

def home_view(request):
    return render(request, 'home.html')



from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from CrudTrabajadores.models import Trabajador

def login_view(request):
    if request.method == 'POST':
        # Usamos 'rut' como 'username' para autenticar
        username = request.POST['rut']  # Asignamos 'rut' a 'username'
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)  # Autenticamos usando 'username'
        
        if user is not None:
            login(request, user)
            
            # Guardar el RUT y el nombre de usuario en la sesión
            if user.is_superuser:
                request.session['trabajador_rut'] = username  # Almacena el RUT del superusuario
                request.session['user'] = user.username  # Guarda el nombre de usuario en la sesión
                return redirect('trabajador-list')  # Redirige a la lista de trabajadores si es superusuario
            
            try:
                # Obtener el trabajador asociado al usuario autenticado
                trabajador = Trabajador.objects.get(user=user)  # Buscamos el trabajador asociado al usuario
                
                # Guardar el RUT y el nombre de usuario en la sesión
                request.session['trabajador_rut'] = trabajador.rut
                request.session['user'] = user.username  # Guarda el nombre de usuario en la sesión
                
                # Redirigir al detalle del trabajador usando su ID
                return redirect('trabajador-detail', pk=trabajador.id)
            except Trabajador.DoesNotExist:
                # Si no existe el trabajador, mostrar un mensaje
                return render(request, 'login.html', {'error': 'No se encuentra trabajador asociado al usuario.'})
        else:
            # Si las credenciales son incorrectas, mostramos un error
            return render(request, 'login.html', {'error': 'Credenciales incorrectas'})
    else:
        return render(request, 'login.html')





def logout_view(request):
    logout(request)  # Cierra la sesión de Django
    request.session.flush()  # Elimina las variables de la sesión de Trabajador
    return redirect('home')  # Redirige al login



def register_view(request):
    if request.method == 'POST':
        form = RegistroTrabajadorForm(request.POST)
        if form.is_valid():
            rut = form.cleaned_data['rut']
            password = form.cleaned_data['password']
            nombre = form.cleaned_data['nombre']
            apellido = form.cleaned_data['apellido']
            
            # Crear el usuario
            user = User.objects.create_user(username=rut, password=password)
            
            # Crear el trabajador
            trabajador = Trabajador(
                rut=rut,
                nombre=nombre,
                apellido=apellido,
                fecha_ingreso="2024-01-01",
                user=user
            )
            trabajador.save()
            
            return redirect('login')
    else:
        form = RegistroTrabajadorForm()
    
    return render(request, 'register.html', {'form': form})

from functools import wraps
from django.shortcuts import redirect

def trabajador_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'trabajador_rut' in request.session:
            return view_func(request, *args, **kwargs)
        return redirect('login')
    return wrapper


