from django.urls import path
from .views import message_view,  choose_login
urlpatterns = [
    path('chat-room/<str:room_name>/', message_view, name='chat'),
    path('choose-login/', choose_login, name='choose_login')
]
