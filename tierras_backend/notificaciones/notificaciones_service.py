import random
from usuarios.models.usuario_rol import UsuarioRol
from notificaciones.models import Notificacion
from notificaciones.notify_user import notify_user
import re

class NotificacionesService:

    @staticmethod
    def generar_seleccion_aleatoria(user_id, beneficiario_id, escritura_id, roles_instance):
        """
        Crea notificaciones para dos jueces (rol_id=5), un notario (rol_id=6),
        el creador y el beneficiario, guardando cada Notificacion como instancia.
        Además actualiza roles_instance con los IDs seleccionados.
        """
        # 1) Selección aleatoria de jueces y notario
        jueces = NotificacionesService._random_user(5, count=2)
        juez1, juez2 = jueces
        notario = NotificacionesService._random_user(6)

        # 2) Lista de destinatarios inicial (jueces, notario y creador)
        destinatarios = [juez1, juez2, notario, user_id]

        # 3) Crear notificaciones y acumular instancias
        notificaciones = []
        for destino in destinatarios:
            notif = Notificacion.objects.create(
                id_escritura_id=escritura_id,
                user_receiver=NotificacionesService.sanitize_group_name(destino),
                user_sender=NotificacionesService.sanitize_group_name(user_id),
                mensaje=f"Se le ha asignado una nueva tarea en la escritura #{escritura_id}"
            )
            notify_user(notif)
            notificaciones.append(notif)

        # 4) Notificación al beneficiario
        notif_ben = Notificacion.objects.create(
            id_escritura_id=escritura_id,
            user_receiver=beneficiario_id,
            user_sender=NotificacionesService.sanitize_group_name(user_id),
            mensaje=f"Su proceso de escritura #{escritura_id} está en curso"
        )
        notify_user(notif_ben)
        notificaciones.append(notif_ben)

        # 5) Actualizar roles_instance y guardar
        roles_instance.id_escribano = user_id
        roles_instance.id_juez1    = juez1
        roles_instance.id_juez2    = juez2
        roles_instance.id_notario  = notario
        roles_instance.save()

        # 6) Devolver tanto la selección de IDs como las instancias
        return {
            'seleccion_ids': {
                'juez1': juez1,
                'juez2': juez2,
                'notario': notario,
                'creador': user_id,
                'beneficiario': beneficiario_id
            },
            'notificaciones': notificaciones
        }

    @staticmethod
    def _random_user(role_id, count=1):
        qs = UsuarioRol.objects.filter(rol_id=role_id).values_list('usuario_id', flat=True)
        user_ids = list(qs)
        if not user_ids:
            raise ValueError(f"No hay usuarios para rol_id={role_id}")

        if count == 1:
            return random.choice(user_ids)
        if count <= len(user_ids):
            return random.sample(user_ids, count)

        raise ValueError(f"Necesitas {count} usuarios para rol_id={role_id}, pero solo hay {len(user_ids)}")

    @staticmethod
    def sanitize_group_name(name):
        # Reemplaza cualquier carácter que no sea alfanumérico, guion, guion bajo o punto
        return re.sub(r'[^a-zA-Z0-9\-_.]', '_', name)
