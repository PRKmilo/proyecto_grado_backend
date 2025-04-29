from django.test import TestCase
from escrituras.models import Escritura
from notificaciones.models import Notificacion
from procesos.models.proceso import Proceso
from datetime import date

class NotificacionModelTest(TestCase):

    def setUp(self):
        # Crear una instancia de Escritura para usar en las pruebas
        proceso = Proceso.objects.create(proceso_id=33, estado="iniciado")
        self.escritura = Escritura.objects.create(
            numero_escritura="ESC100",
            fecha_otorgamiento=date(2023, 5, 10),
            proceso_escritura=proceso
        )

    def test_creacion_notificacion_basica(self):
        """Prueba la creación básica de una notificación con todos los campos."""
        notificacion = Notificacion.objects.create(
            id_escritura=self.escritura,
            user_sender="usuario_emisor",
            user_receiver="usuario_receptor",
            mensaje="Mensaje de prueba"
        )
        # Validaciones explícitas para cada campo
        self.assertEqual(notificacion.user_sender, "usuario_emisor")
        self.assertEqual(notificacion.user_receiver, "usuario_receptor")
        self.assertEqual(notificacion.mensaje, "Mensaje de prueba")
        self.assertEqual(notificacion.id_escritura, self.escritura)

    def test_campos_opcionales_nulos(self):
        """Prueba la creación de una notificación con campos opcionales nulos."""
        notificacion = Notificacion.objects.create(
            id_escritura=self.escritura
        )
        # Comprobamos que los campos opcionales son None
        self.assertIsNone(notificacion.user_sender)
        self.assertIsNone(notificacion.user_receiver)
        self.assertIsNone(notificacion.mensaje)

    def test_relacion_con_escritura(self):
        """Verifica que la notificación esté correctamente relacionada con una escritura."""
        notificacion = Notificacion.objects.create(
            id_escritura=self.escritura,
            mensaje="Notificación relacionada"
        )
        # Verificación de la relación con la escritura
        self.assertEqual(notificacion.id_escritura.numero_escritura, "ESC100")

    def test_creacion_notificacion_sin_escritura(self):
        """Verifica que una notificación pueda ser creada sin una escritura asociada."""
        notificacion = Notificacion.objects.create(
            user_sender="usuario_emisor",
            user_receiver="usuario_receptor",
            mensaje="Mensaje sin escritura"
        )

        # Verificar que la notificación se crea correctamente
        self.assertEqual(notificacion.user_sender, "usuario_emisor")
        self.assertEqual(notificacion.user_receiver, "usuario_receptor")
        self.assertEqual(notificacion.mensaje, "Mensaje sin escritura")
        self.assertIsNone(notificacion.id_escritura)  # Verifica que no esté asociada a ninguna escritura   
