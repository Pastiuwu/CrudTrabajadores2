from django.contrib import admin
from .models import Trabajador, Departamento, Area, CargaFamiliar

#register 

admin.site.register(Trabajador)
admin.site.register(Departamento)
admin.site.register(Area)
admin.site.register(CargaFamiliar)
