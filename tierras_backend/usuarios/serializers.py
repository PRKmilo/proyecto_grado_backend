from rest_framework import serializers
from .models import Usuario, MFADevice

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'


class MFASerializer(serializers.ModelSerializer):
    class Meta:
        model = MFADevice
        fields = ["secret", "is_active"]
