from django.contrib.auth.backends import BaseBackend
from .models import Usuario
from .authentication import AuthenticationService  # Importamos el servicio de autenticación

class CustomAuthBackend(BaseBackend):
    def authenticate(self, request, cedula=None, password=None):
        """Autentica al usuario utilizando AuthenticationService."""
        usuario = AuthenticationService.autenticar_usuario(cedula, password)
        return usuario  # Retorna el usuario autenticado o None si falla

    def get_user(self, user_id):
        """Obtiene un usuario por su ID (cédula en este caso)."""
        try:
            return Usuario.objects.get(cedula=user_id)
        except Usuario.DoesNotExist:
            return None
