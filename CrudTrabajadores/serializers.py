from rest_framework import serializers
from .models import Trabajador, Departamento, Area, CargaFamiliar

class TrabajadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trabajador
        fields = '__all__'

class DepartamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departamento
        fields = '__all__'

class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = '__all__'

class CargaFamiliarSerializer(serializers.ModelSerializer):
    class Meta:
        model = CargaFamiliar
        fields = '__all__'
