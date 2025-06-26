from django.urls import path
from . import views

urlpatterns = [
    path('default', views.index, {'room_name': 'default_room'}, name='video_default'),
    path('<str:room_name>/', views.index, name='index'),  # ✅ expects room_name
]