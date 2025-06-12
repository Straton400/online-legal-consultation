from django.shortcuts import render, redirect
from .models import Room,Message

# Create your views here.


def CreateRoom(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        room = request.POST.get('room')

        try:
            # Try to get the room if it exists
            get_room = Room.objects.get(room_name=room)
        except Room.DoesNotExist:
            # If it doesn't exist, create a new one
            get_room = Room.objects.create(room_name=room)
        
        # Redirect to the chat room
        return redirect('room', room_name=room, username=username)

    # Render the create room page if not POST request
    return render(request, 'chatapp/index.html')



from django.shortcuts import get_object_or_404
from .models import Room, Message
from consultation_app.models import Client, Lawyer  # update with your actual app name

def MessageView(request, room_name, username):
    # Get the room (or create it if it doesn't exist)
    get_room, _ = Room.objects.get_or_create(room_name=room_name)

    # Get all messages for that room
    get_messages = Message.objects.filter(room=get_room)

    # If username is blank, fetch it from logged-in client/lawyer session
    if not username:
        if request.session.get('client_id'):
            client = get_object_or_404(Client, id=request.session['client_id'])
            username = client.email
        elif request.session.get('lawyer_id'):
            lawyer = get_object_or_404(Lawyer, id=request.session['lawyer_id'])
            username = lawyer.username
        else:
            return redirect('login')  # fallback if not logged in

    context = {
        "messages": get_messages,
        "user": username,
        "room_name": room_name,
    }

    return render(request, 'chatapp/message.html', context)


from django.shortcuts import render, get_object_or_404
from .models import Room

def chat_room(request, room_name):
    room = get_object_or_404(Room, room_name=room_name)
    return render(request, 'chatapp/message.html', {'room': room})

def chat_room_view(request, room_name):
    room = get_object_or_404(Room, room_name=room_name)
    return render(request, 'ChatApp/message.html', {'room': room})
