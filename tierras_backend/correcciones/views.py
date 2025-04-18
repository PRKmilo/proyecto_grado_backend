# notificaciones/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Correcion

class CorreccionView(APIView):
    """
    GET /api/correcciones/<user_id>/
    Devuelve una lista de correcciones pertenecientes a notificaciones 
    donde el usuario es receptor, pero solo con los campos que necesitas.
    """
    def get(self, request, user_id):
        # Filtramos las correcciones por user_receiver
        qs = Correcion.objects.filter(
            id_notificacion__user_receiver=str(user_id)
        )

        # Construimos la lista con solo los campos requeridos
        data = [
            {
                'id_correcion'   : c.id_correcion,
                'descripcion'    : c.descripcion,
                'comentario'     : c.comment,
                'linea'          : c.line_number,
                'inicio'         : c.start_position,
                'fin'            : c.end_position,
                'resuelto'       : c.is_resolved,
            }
            for c in qs
        ]

        return Response(data)
        
