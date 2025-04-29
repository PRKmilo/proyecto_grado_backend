from django.test import TestCase
from correcciones.models import Correcion
from notificaciones.models import Notificacion

class CorrecionModelTest(TestCase):
    def setUp(self):
        # Creamos una notificación de prueba para relacionar
        self.notificacion = Notificacion.objects.create(
            user_sender="1001232432",
            user_receiver="100232433",
            mensaje="esta es una notificacion de prueba"
        )

    def test_crear_correcion_valida(self):
        """Verifica que se puede crear una corrección válida."""
        correcion = Correcion.objects.create(
            id_notificacion=self.notificacion,
            line_number=10,
            start_position=5,
            end_position=15,
            is_resolved=False,
            comment="Hay un error en el texto.",
            descripcion="Se debe corregir el nombre del propietario."
        )

        self.assertEqual(correcion.line_number, 10)
        self.assertFalse(correcion.is_resolved)
        self.assertEqual(correcion.comment, "Hay un error en el texto.")
        self.assertEqual(correcion.id_notificacion, self.notificacion)

    def test_campo_comment_puede_ser_nulo(self):
        """Verifica que el campo comment puede ser null o vacío."""
        correcion = Correcion.objects.create(
            id_notificacion=self.notificacion,
            line_number=1,
            start_position=0,
            end_position=5,
            is_resolved=True,
            comment=None,
            descripcion="Solo descripción"
        )
        self.assertIsNone(correcion.comment)

    def test_campo_descripcion_puede_ser_nulo(self):
        """Verifica que el campo descripcion puede ser null o vacío."""
        correcion = Correcion.objects.create(
            id_notificacion=self.notificacion,
            line_number=2,
            start_position=3,
            end_position=8,
            is_resolved=True,
            comment="Comentario sin descripción",
            descripcion=None
        )
        self.assertIsNone(correcion.descripcion)

    def test_string_representation(self):
        """Puedes agregar una representación string opcional si lo deseas."""
        correcion = Correcion.objects.create(
            id_notificacion=self.notificacion,
            line_number=3,
            start_position=1,
            end_position=4,
            is_resolved=False,
            comment="Error menor",
            descripcion="Corrección menor"
        )
        self.assertEqual(str(correcion), f'Corrección {correcion.id_correcion}')

