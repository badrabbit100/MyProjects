import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from main.consumer import GameRoom
from django.urls import path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'seeab.settings')

django_asgi_app = get_asgi_application()

ws_pattern = [
    path('ws/game/<room_code>', GameRoom.as_asgi())
]

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        'websocket': AuthMiddlewareStack(URLRouter(ws_pattern))
    }
)