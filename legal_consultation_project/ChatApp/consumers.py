import json
import base64
import os
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.core.files.base import ContentFile
from ChatApp.models import Room, Message
from django.conf import settings


class ChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.room_name = f"room_{self.scope['url_route']['kwargs']['room_name']}"
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message')
        sender = text_data_json.get('sender')
        room_name = text_data_json.get('room_name')
        file_data = text_data_json.get('file_data')
        file_name = text_data_json.get('file_name')
        file_type = text_data_json.get('file_type')
        
        file_url = None
        
        if file_data and file_name:
            # Generate a unique filename and save the file
            file_url = await self.save_file(file_data, file_name)

        # Prepare the event to be sent to the group
        event = {
            'type': 'send_message',
            'message': {
                'sender': sender,
                'message': message,
                'room_name': room_name,
                'file_url': file_url
            }
        }
        await self.channel_layer.group_send(self.room_name, event)

    async def send_message(self, event):
        data = event['message']
        await self.create_message(data=data)
        
        # Send back the message, including the file URL if it exists
        response_data = {
            'sender': data['sender'],
            'message': data['message'],
            'file_url': data.get('file_url')
        }
        await self.send(text_data=json.dumps({'message': response_data}))

    @database_sync_to_async
    def create_message(self, data):
        """ Save the message to the database """
        get_room_by_name = Room.objects.get(room_name=data['room_name'])
        new_message = Message(
            room=get_room_by_name,
            sender=data['sender'],
            message=data['message']
        )
        
        if data.get('file_url'):
            new_message.file = data['file_url']
        
        new_message.save()

    @database_sync_to_async
    def save_file(self, file_data, file_name):
        """ Save the Base64 file and return its URL """
        format, file_str = file_data.split(';base64,')
        decoded_file = base64.b64decode(file_str)

        # Create a unique path to store the file
        file_path = os.path.join('uploads', file_name)
        full_path = os.path.join(settings.MEDIA_ROOT, file_path)
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        # Save the file to the media directory
        with open(full_path, 'wb') as file:
            file.write(decoded_file)
        
        # Return the media URL for display
        return os.path.join(settings.MEDIA_URL, file_path)







