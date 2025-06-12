from . import views
from django.urls import path
from .views import chat_room_view,MessageView

urlpatterns = [
    path('', views.CreateRoom, name='create-room'),
    path('<str:room_name>/<str:username>/', views.MessageView, name='room'),
    path('chat-room/<str:room_name>/<str:username>/', views.MessageView, name='room'),

    path('chat/<str:room_name>/', MessageView, name='chat-room'),
    path('chat-room/<str:room_name>/<str:username>/', views.MessageView, name='room'),

   path('live-chat/chat-room/<str:room_name>/<str:username>/', views.MessageView, name='room'),


]