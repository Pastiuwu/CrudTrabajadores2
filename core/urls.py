from django.urls import path
from CrudTrabajadores import views as trabajadores_views  # Importar las vistas de CrudTrabajadores con un alias
from . import views
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('trabajadores/', trabajadores_views.trabajador_list, name='trabajador-list'),
]
