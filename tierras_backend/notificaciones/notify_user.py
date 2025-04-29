from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from notificaciones.models import Notificacion
from notificaciones.serializers import NotificacionSerializer  # o dict manual
import re
def notify_user(notif_instance):
    channel_layer = get_channel_layer()
    name_group=re.sub(r'[^a-zA-Z0-9\-_.]', '_', notif_instance.user_receiver)
    group_name = f'notifications_{name_group}'
    
    # Si tienes un serializer:
    from notificaciones.serializers import NotificacionSerializer
    


    payload = {
        'id_notificacion': notif_instance.id_notificacion,
        'mensaje'        : notif_instance.mensaje,
        # puedes añadir aquí más campos que necesites
    }


    

    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'send_notification',  # coincide con el método en el Consumer
            'payload': payload,
        }
    )
