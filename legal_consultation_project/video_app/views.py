# video_app/views.py

from django.shortcuts import render

def index(request, room_name):
    print(f"Room name: {room_name}")
    return render(request, 'video_app/index.html', {'room_name': room_name})