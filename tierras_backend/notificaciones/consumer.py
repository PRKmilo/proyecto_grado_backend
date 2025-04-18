import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            print("llega a conexion socket")
            self.user_id = self.scope['url_route']['kwargs']['user_id']
            self.group_name = f'notifications_{self.user_id}'

            # Únete al grupo de notificaciones de este usuario
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            print(f"Unido al grupo: {self.group_name}")
            await self.accept()
        except Exception as e:
            print(f"Error en connect():" {e})
            raise 

    async def disconnect(self, close_code):
        print("se desconecta el socket")
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    # Este método se invoca cuando alguien hace group_send(...)
    async def send_notification(self, event):
        # event['payload'] contendrá la serialización de tu instancia
        print("se ingresa a send_notificacion")
        await self.send(text_data=json.dumps(event['payload']))
