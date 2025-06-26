# video_chat_core/routing.py

from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from video_app.consumers import VideoChatConsumer # <--- We'll create this consumer next, notice 'video_app'
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
     re_path(r'ws/video_chat/(?P<room_name>\w+)/$', consumers.VideoChatConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    'websocket': URLRouter(websocket_urlpatterns),
})