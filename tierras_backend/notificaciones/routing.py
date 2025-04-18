from django.urls import re_path
from . import consumer

websocket_urlpatterns = [
    # Un WebSocket por usuario; usaremos user_id como path
        re_path(r'ws/notifications/(?P<user_id>\w+)/$', consumer.NotificationConsumer.as_asgi())
]

