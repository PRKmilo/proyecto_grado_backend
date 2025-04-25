from django.test import TestCase
from django.db import IntegrityError
from usuarios.models import Usuario


class UsuarioModelTest(TestCase):

    def setUp(self):
        """Configuración inicial para las pruebas."""
        # Crea un usuario con los campos requeridos
        self.usuario = Usuario.objects.create(
            cedula="123456789",
            hash_password="hashedpassword123",
            username="juanperez",
            nombre="Juan Pérez",
            primer_apellido="Pérez",
            segundo_apellido="López",
            fecha_expedicion_cedula="2000-01-01",
            email="juan@example.com",
            nt="NT001"
        )

    def test_creacion_usuario_basica(self):
        """Prueba la creación básica de un usuario con todos los campos."""
        usuario = Usuario.objects.create(
            cedula="987654321",
            hash_password="hashedpassword456",
            username="anagomez",
            nombre="Ana Gómez",
            primer_apellido="Gómez",
            segundo_apellido="Díaz",
            fecha_expedicion_cedula="2005-05-15",
            email="ana@example.com",
            nt="NT002"
        )
        self.assertEqual(usuario.nombre, "Ana Gómez")
        self.assertEqual(usuario.email, "ana@example.com")
        self.assertEqual(usuario.cedula, "987654321")
        self.assertEqual(usuario.fecha_expedicion_cedula, "2005-05-15")

    def test_usuario_sin_email(self):
        """Verifica que no se pueda crear un usuario sin un email."""
        with self.assertRaises(IntegrityError):
            Usuario.objects.create(
                cedula="111223344",
                hash_password="hashedpassword789",
                username="luismartin",
                nombre="Luis Martín",
                primer_apellido="Martín",
                segundo_apellido="Gómez",
                fecha_expedicion_cedula="2010-03-25",
                nt="NT003"
            )

    def test_usuario_con_email_unico(self):
        """Verifica que no se pueda crear un usuario con un email duplicado."""
        Usuario.objects.create(
            cedula="123123123",
            hash_password="hashedpassword123",
            username="carlosdiaz",
            nombre="Carlos Díaz",
            primer_apellido="Díaz",
            segundo_apellido="Sánchez",
            fecha_expedicion_cedula="2011-02-20",
            email="carlos@example.com",
            nt="NT004"
        )
        with self.assertRaises(IntegrityError):
            Usuario.objects.create(
                cedula="987987987",
                hash_password="hashedpassword456",
                username="sofiaherrera",
                nombre="Sofia Herrera",
                primer_apellido="Herrera",
                segundo_apellido="Pérez",
                fecha_expedicion_cedula="2012-07-30",
                email="carlos@example.com",  # Email duplicado
                nt="NT005"
            )

    def test_usuario_sin_fecha_expedicion_cedula(self):
        """Verifica que un usuario pueda ser creado sin especificar la fecha de expedición de la cédula."""
        usuario = Usuario.objects.create(
            cedula="555555555",
            hash_password="hashedpassword000",
            username="pedrosanchez",
            nombre="Pedro Sánchez",
            primer_apellido="Sánchez",
            segundo_apellido="Martínez",
            email="pedro@example.com",
            nt="NT006"
        )
        self.assertIsNone(usuario.fecha_expedicion_cedula)

    def test_creacion_usuario_con_campos_opcionales(self):
        """Prueba la creación de un usuario con campos opcionales."""
        usuario = Usuario.objects.create(
            cedula="333333333",
            hash_password="hashedpassword789",
            username="laurarodriguez",
            nombre="Laura Rodríguez",
            primer_apellido="Rodríguez",
            segundo_apellido="Gómez",
            fecha_expedicion_cedula=None,
            email="laura@example.com",
            nt="NT007"
        )
        self.assertEqual(usuario.nombre, "Laura Rodríguez")
        self.assertEqual(usuario.email, "laura@example.com")
        self.assertIsNone(usuario.fecha_expedicion_cedula)  # Verifica que la fecha sea None

    def test_validacion_cedula_unico(self):
        """Verifica que el campo cedula sea único."""
        usuario1 = Usuario.objects.create(
            cedula="9999",
            hash_password="hashedpassword111",
            username="ricardogomez",
            nombre="Ricardo Gómez",
            primer_apellido="Gómez",
            segundo_apellido="López",
            fecha_expedicion_cedula="2015-09-10",
            email="ricardo@example.com",
            nt="NT008"
        )

        with self.assertRaises(IntegrityError):
            Usuario.objects.create(
                cedula="9999",  # misma cédula = clave primaria duplicada
                hash_password="hashedpassword222",
                username="sofiaherrera",
                nombre="Sofia Herrera",
                segundo_apellido="Pérez",
                fecha_expedicion_cedula="2016-03-20",
                email="sofia@example.com",
                nt="NT009"
            )
