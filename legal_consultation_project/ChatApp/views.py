from django.shortcuts import render, redirect, get_object_or_404
from .models import Room, Message
from consultation_app.models import Client, Lawyer
def message_view(request, room_name):
    room, _ = Room.objects.get_or_create(room_name=room_name)

    sender_id = request.session.get('user_id')
    sender_type = request.session.get('user_type')
    sender_name = None

    if sender_type == 'client':
        client = Client.objects.filter(id=sender_id).first()
        if client:
            sender_name = client.first_name or client.email
        else:
            return redirect('client_login')
    elif sender_type == 'lawyer':
        lawyer = Lawyer.objects.filter(id=sender_id).first()
        if lawyer:
            sender_name = lawyer.username
        else:
            return redirect('lawyer_login')
    else:
        # Could be redirect to a landing/login page instead of hardcoded lawyer login
        return redirect('client_login')

    messages = Message.objects.filter(room=room).order_by('timestamp')

    return render(request, 'chatapp/message.html', {
        'room_name': room_name,
        'messages': messages,
        'sender_id': sender_id,
        'sender_type': sender_type,
        'sender_name': sender_name,
    })

def choose_login(request):
    return render(request, 'consultation_app/choose_login.html')
