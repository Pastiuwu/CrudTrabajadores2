from django.contrib.auth.models import User
from django.db import models
from core.validators import validate_rut, validate_nombre_apellido, validate_fecha_ingreso

class Departamento(models.Model):
    nombre_departamento = models.CharField(max_length=50, blank=False)
    ubicacion = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return self.nombre_departamento

class Area(models.Model):
    TIPO_AREA_CHOICES = [
        ('Marketing', 'Marketing'),
        ('Finanzas', 'Finanzas'),
        ('Logistica', 'Logística'),
        ('IT', 'IT'),
        ('Ventas', 'Ventas'),
        ('Administrativa', 'Administrativa'),
    ]
    nombre_area = models.CharField(max_length=50, blank=False)
    tipo_area = models.CharField(max_length=50, choices=TIPO_AREA_CHOICES, blank=False)

    def __str__(self):
        return self.nombre_area

class CargaFamiliar(models.Model):
    nombre_carga = models.CharField(max_length=50, blank=False)
    relacion = models.CharField(max_length=50, blank=False)
    GRUPO_SALUD_CHOICES = [
        ('Fonasa', 'Fonasa'),
        ('Isapre', 'Isapre'),
    ]
    grupo_salud = models.CharField(max_length=50, choices=GRUPO_SALUD_CHOICES, blank=False)

    def __str__(self):
        return self.nombre_carga

class Trabajador(models.Model):
    rut = models.CharField(
        max_length=12, 
        unique=True, 
        blank=True, 
        null=True, 
        validators=[validate_rut]
    )
    nombre = models.CharField(
        max_length=50, 
        blank=False, 
        validators=[validate_nombre_apellido]
    )
    apellido = models.CharField(
        max_length=50, 
        blank=False, 
        validators=[validate_nombre_apellido]
    )
    fecha_ingreso = models.DateField(validators=[validate_fecha_ingreso])
    estado_activo = models.BooleanField(default=True)

    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, null=True)
    area = models.ForeignKey(Area, on_delete=models.CASCADE, null=True)
    cargas_familiar = models.ForeignKey(CargaFamiliar, on_delete=models.CASCADE, null=True)
    
    # modelo User de Django
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.rut}"
