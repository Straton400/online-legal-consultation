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



def MessageView(request, room_name, username):
    get_room = Room.objects.get(room_name=room_name)
    get_messages = Message.objects.filter(room=get_room)
    
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
