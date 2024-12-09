import re
from django.core.exceptions import ValidationError
from datetime import date

def validate_rut(value):
    pattern = r'^\d{1,2}\.\d{3}\.\d{3}-[0-9kK]$'
    if not re.match(pattern, value):
        raise ValidationError(f"El RUT '{value}' no tiene un formato válido. Ejemplo: 12.345.678-9.")

def validate_nombre_apellido(value):
    if not re.match(r'^[a-zA-Z\s]+$', value):
        raise ValidationError(f"'{value}' solo puede contener letras y espacios.")

def validate_fecha_ingreso(value):
    if value > date.today():
        raise ValidationError("La fecha de ingreso no puede ser una fecha futura.")
