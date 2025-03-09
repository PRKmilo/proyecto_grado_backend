from rest_framework import serializers
from .models import Escritura

class EscrituraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Escritura
        fields = '__all__'  # O puedes especificar campos ['campo1', 'campo2']
