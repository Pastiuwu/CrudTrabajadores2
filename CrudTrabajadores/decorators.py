from functools import wraps
from django.shortcuts import redirect

def trabajador_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Verificar si el trabajador está logueado mediante la sesión
        if 'trabajador_rut' in request.session:
            return view_func(request, *args, **kwargs)
        return redirect('login')  # Redirigir al login si no está autenticado
    return wrapper
