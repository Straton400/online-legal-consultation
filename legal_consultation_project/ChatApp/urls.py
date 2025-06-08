from . import views
from django.urls import path
from .views import chat_room_view

urlpatterns = [
    path('', views.CreateRoom, name='create-room'),
    path('<str:room_name>/<str:username>/', views.MessageView, name='room'),

    #path('room/<str:room_name>/', views.chat_room, name='chat_room'),
]