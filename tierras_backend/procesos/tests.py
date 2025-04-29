from django.test import TestCase
from procesos.models import Proceso
from usuarios.models import Usuario
from datetime import date

class ProcesoModelTest(TestCase):

    def setUp(self):
        self.usuario = Usuario.objects.create(
            cedula="1234567890",
            username="juanperez",
            hash_password="hash123",
            nombre="Juan",
            primer_apellido="Pérez",
            segundo_apellido="Gómez",
            fecha_expedicion_cedula="2010-01-01",
            email="juan@example.com",
            nt="NT001"
        )

    def test_crear_proceso_valido(self):
        proceso = Proceso.objects.create(
            usuario=self.usuario,
            seriado_proceso="PRC1234",
            estado="En curso",
            fecha_inicio=date(2024, 4, 22),
            fecha_actualizacion=date(2024, 4, 22),
            limite_tiempo=30,
            fecha_limite=date(2024, 5, 22)
        )
        self.assertIsInstance(proceso, Proceso)
        self.assertEqual(proceso.estado, "En curso")
        self.assertEqual(proceso.usuario.cedula, "1234567890")

    def test_campo_seriado_proceso_puede_ser_nulo(self):
        proceso = Proceso.objects.create(usuario=self.usuario)
        self.assertIsNone(proceso.seriado_proceso)

    def test_campo_fecha_limite_puede_ser_nulo(self):
        proceso = Proceso.objects.create(usuario=self.usuario)
        self.assertIsNone(proceso.fecha_limite)

    def test_proceso_puede_crearse_sin_usuario(self):
        proceso = Proceso.objects.create(estado="Sin usuario")
        self.assertIsNone(proceso.usuario)

    def test_limite_tiempo_es_numero_entero(self):
        proceso = Proceso.objects.create(
            usuario=self.usuario,
            limite_tiempo=45
        )
        self.assertEqual(proceso.limite_tiempo, 45)

    def test_string_representation(self):
        proceso = Proceso.objects.create(
            usuario=self.usuario,
            seriado_proceso="PROC-456"
        )
        self.assertEqual(str(proceso), f"Proceso {proceso.proceso_id} - PROC-456")
