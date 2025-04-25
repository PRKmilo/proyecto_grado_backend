from django.test import TestCase
from usuarios.models import Usuario
from procesos.models import Proceso
from escrituras.models import Escritura
from datetime import date

class EscrituraModelTest(TestCase):

    def setUp(self):
        # Crear un usuario simulado
        self.usuario = Usuario.objects.create_user(
            cedula="1234567890",
            username="testuser",
            password="securepassword",
            nombre="Juan",
            primer_apellido="Pérez",
            segundo_apellido="López",
            email="juan@example.com"
        )

        # Crear un proceso relacionado al usuario
        self.proceso = Proceso.objects.create(
            usuario=self.usuario,
            seriado_proceso="PROC-001",
            estado="Activo",
            fecha_inicio=date(2023, 1, 1),
            fecha_actualizacion=date(2023, 1, 10),
            limite_tiempo=30,
            fecha_limite=date(2023, 2, 1)
        )

    def test_creacion_escritura_minima(self):
        escritura = Escritura.objects.create(
            numero_escritura="ESC001",
            proceso_escritura=self.proceso
        )
        self.assertEqual(escritura.numero_escritura, "ESC001")
        self.assertEqual(escritura.proceso_escritura, self.proceso)

    def test_creacion_escritura_completa(self):
        escritura = Escritura.objects.create(
            numero_escritura="ESC002",
            proceso_escritura=self.proceso,
            nombre_notaria="Notaría 12",
            fecha_otorgamiento=date(2023, 3, 5),
            fecha_inicio=date(2023, 3, 1),
            municipio="Duitama",
            descripcion_movimiento="Venta predio rural",
            direccion_predio="Vereda El Retiro, Lote 4",
            direccion_smart_contract="0xabc123",
            direccion_temporal_data="IPFS_HASH_X",
            direccion_temporal_data2="IPFS_HASH_Y",
            cedula_catastral="CAT123456789"
        )
        self.assertEqual(escritura.nombre_notaria, "Notaría 12")
        self.assertEqual(escritura.municipio, "Duitama")
        self.assertEqual(escritura.proceso_escritura.seriado_proceso, "PROC-001")

    def test_campos_opcionales_nulos(self):
        escritura = Escritura.objects.create(
            numero_escritura="ESC003",
            proceso_escritura=self.proceso
        )
        self.assertIsNone(escritura.nombre_notaria)
        self.assertIsNone(escritura.direccion_predio)
        self.assertIsNone(escritura.direccion_smart_contract)

    def test_relacion_proceso_usuario(self):
        escritura = Escritura.objects.create(
            numero_escritura="ESC004",
            proceso_escritura=self.proceso
        )
        self.assertEqual(escritura.proceso_escritura.usuario, self.usuario)
        self.assertEqual(escritura.proceso_escritura.usuario.nombre, "Juan")
