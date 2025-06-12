from django.urls import path
from . import views

urlpatterns = [
    path('<int:consultation_id>/', views.video_chat_room, name='video_chat_room'),
    

]
