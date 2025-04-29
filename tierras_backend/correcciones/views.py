# notificaciones/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Correcion

class CorreccionView(APIView):

    def get(self, request, user_id):
        # Filtramos las correcciones por user_receiver
        qs = Correcion.objects.filter(
            id_notificacion__user_receiver=str(user_id)
        )

        # Construimos la lista con los campos de Correcion + datos de Notificacion
        data = [
            {
                'id_correcion'    : c.id_correcion,
                'descripcion'     : c.descripcion,
                'comentario'      : c.comment,
                'linea'           : c.line_number,
                'inicio'          : c.start_position,
                'fin'             : c.end_position,
                'resuelto'        : c.is_resolved,

                # Datos de la notificación asociada
                'notificacion': {
                    'id'             : c.id_notificacion.id_notificacion,
                    'mensaje'        : c.id_notificacion.mensaje,
                    'emisor'         : c.id_notificacion.user_sender,
                    'receptor'       : c.id_notificacion.user_receiver,
                    'id_escritura'   : c.id_notificacion.id_escritura_id,
                    'fecha_envio'    : c.id_notificacion.created_at.strftime('%Y-%m-%d %H:%M:%S') 
                                       if hasattr(c.id_notificacion, 'created_at') else None
                }
            }
            for c in qs
        ]

        return Response(data)
