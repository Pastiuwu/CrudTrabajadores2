from django import forms
import re
from .models import Trabajador, Departamento, Area, CargaFamiliar
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class RegistroTrabajadorForm(forms.Form):
    rut = forms.CharField(max_length=12, required=True, label="RUT")
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    nombre = forms.CharField(max_length=100, required=True, label="Nombre")
    apellido = forms.CharField(max_length=100, required=True, label="Apellido")

    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        
        # Eliminar puntos y guiones del RUT para validación
        rut_cleaned = rut.replace(".", "").replace("-", "")
        
        # Validar formato con regex
        if not re.match(r'^\d{7,8}[0-9kK]$', rut_cleaned):
            raise ValidationError("El formato del RUT no es válido. Ejemplo: 12.345.678-9")
        
        
        
        # Validar si el RUT ya existe
        if Trabajador.objects.filter(rut=rut).exists():
            raise ValidationError("Este RUT ya está registrado.")
        return rut



class TrabajadorForm(forms.ModelForm):
    class Meta:
        model = Trabajador
        fields = ['rut', 'nombre', 'apellido', 'fecha_ingreso', 'estado_activo', 'departamento', 'area', 'cargas_familiar']


class DepartamentoForm(forms.ModelForm):
    class Meta:
        model = Departamento
        fields = '__all__'


class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = '__all__'


class CargaFamiliarForm(forms.ModelForm):
    class Meta:
        model = CargaFamiliar
        fields = '__all__'
