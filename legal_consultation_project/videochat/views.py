from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def video_chat_room(request, room_name):
    return render(request, 'videochat/videochat.html', {'room_name': room_name})


from django.shortcuts import render, get_object_or_404, redirect
from consultation_app.models import Consultation  # or wherever your model is defined

@login_required
def video_chat_room(request, consultation_id):
    consultation = get_object_or_404(Consultation, id=consultation_id)

    # Only allow access if consultation is accepted
    if consultation.status != 'accepted':
        return redirect('consultation_denied')  # still prevents access to unapproved consultations

    room_name = consultation.get_video_room_name()  # or get_room_name if that's the method
    return render(request, 'videochat/videochat.html', {'room_name': room_name})
