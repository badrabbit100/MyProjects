from django.urls import re_path
from .consumer import GameRoom

websocket_urlpatterns = [
    re_path(r'ws/game/<room_number>', GameRoom),
]
