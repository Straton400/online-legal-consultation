from django.urls import path
from .consumers import ChatConsumer
from django.urls import re_path
from . import consumers 

websocket_urlpatterns = [
    path('ws/notification/<str:room_name>/', ChatConsumer.as_asgi()),
    
   
]