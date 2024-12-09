from django.urls import path
from CrudTrabajadores import views as trabajadores_views 
from .views import listar_trabajador
from core import views as core_views


urlpatterns = [
    # Página principal
    path('', core_views.home_view, name='home'),

    # Página de login
    path('login/', core_views.login_view, name='login'),  # Cambié la ruta a 'login/'

    # Rutas de trabajadores
    
    path('trabajadores/', trabajadores_views.trabajador_list, name='trabajador-list'),
    path('trabajadores/<int:pk>/', trabajadores_views.trabajador_detail, name='trabajador-detail'),
    path('trabajadores/create/', trabajadores_views.trabajador_create, name='trabajador-create'),
    path('trabajadores/<int:pk>/edit/', trabajadores_views.trabajador_update, name='trabajador-update'),
    path('trabajadores/<int:pk>/delete/', trabajadores_views.trabajador_delete, name='trabajador-delete'),
    

    # Rutas de carga familiar
    path('carga-familiar/create/', trabajadores_views.carga_familiar_create, name='carga-familiar-create'),
    path('carga-familiar/update/<int:pk>/', trabajadores_views.carga_familiar_update, name='carga-familiar-update'),

    # Ruta de logout
    path('logout/', core_views.logout_view, name='logout'),
]
