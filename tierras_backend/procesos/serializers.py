from rest_framework import serializers
from .models import Proceso

class ProcesoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proceso
        fields = '__all__'  # O puedes especificar campos ['campo1', 'campo2']
