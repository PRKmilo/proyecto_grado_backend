import jwt
import bcrypt
import datetime
from django.conf import settings
from .models import Usuario

class AuthenticationService:

    @staticmethod
    def generar_jwt(user):
        payload = {
            "user_id": user.cedula,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2),
            "iat": datetime.datetime.utcnow(),
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
        return token

    @staticmethod
    def autenticar_usuario(cedula, password):
        try:
            usuario = Usuario.objects.get(cedula=cedula)
            if bcrypt.checkpw(password.encode(), usuario.hash_password.encode()):
                return usuario
        except Usuario.DoesNotExist:
            pass
        return None
