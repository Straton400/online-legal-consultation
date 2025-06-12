from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def video_chat_room(request, room_name):
    return render(request, 'videochat/videochat.html', {'room_name': room_name})


from django.shortcuts import render, get_object_or_404, redirect
from consultation_app.models import Consultation  # or wherever your model is defined


from django.contrib.auth.decorators import login_required

from consultation_app.models import Client, Lawyer  # adjust to your actual app name

def video_chat_room(request, consultation_id):
    consultation = get_object_or_404(Consultation, id=consultation_id)

    if consultation.status != 'accepted':
        return redirect('consultation_denied')

    room_name = consultation.get_video_room_name()

    username = request.session.get('username')
    if not username:
        return redirect('login')  # fallback if session lost

    return render(request, 'videochat/videochat.html', {
        'room_name': room_name,
        'username': username,
    })
