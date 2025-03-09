from django.contrib.auth.models import AbstractUser
import pyotp
import bcrypt
from django.db import models

class Usuario(AbstractUser):
    cedula = models.CharField(primary_key=True, max_length=255)
    hash_password = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    nombre = models.CharField(max_length=255, blank=True, null=True)
    primer_apellido = models.CharField(max_length=255, blank=True, null=True)
    segundo_apellido = models.CharField(max_length=255, blank=True, null=True)
    fecha_expedicion_cedula = models.DateField(blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    nt = models.CharField(max_length=255, blank=True, null=True)

    #is_active = models.BooleanField(default=True)
    #is_staff = models.BooleanField(default=False)
    #is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = "cedula"  # Ahora la autenticación se hará con 'cedula'
    REQUIRED_FIELDS = ["username", "email"]
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="usuarios",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="usuarios_permisos",
        blank=True
    )
    class Meta:
        managed = True
        db_table = 'usuario'

class MFADevice(models.Model):
    user = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name="mfa_device")
    secret = models.CharField(max_length=32, unique=True)
    is_active = models.BooleanField(default=False)

    def generate_totp_uri(self):
        return pyotp.totp.TOTP(self.secret).provisioning_uri(self.user.email, issuer_name="MiApp")

    def verify_code(self, code):
        return pyotp.TOTP(self.secret).verify(code)
