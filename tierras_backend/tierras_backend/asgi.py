import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import notificaciones.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tierras_backend.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(
        notificaciones.routing.websocket_urlpatterns
    ),
})

