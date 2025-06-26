import json
import base64
import os
import uuid
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from .models import Room, Message
from consultation_app.models import Client, Lawyer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.group_name = f"chat_{self.room_name}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("message", "")
        file_data = data.get("file_data")
        file_name = data.get("file_name")
        sender_type = data.get("sender_type")  # safer get()
        sender_id = data.get("sender_id")

        file_url = None
        if file_data and file_name:
            file_url = await self.save_file(file_data, file_name)

        saved_msg = await self.save_message(message, sender_type, sender_id, file_url)
        sender_name = await self.get_sender_name(sender_type, sender_id)

        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chat_message",
                "message": message,
                "file_url": file_url,
                "sender_type": sender_type,
                "sender_id": sender_id,
                "sender_name": sender_name,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": {
                "message": event["message"],
                "file_url": event["file_url"],
                "sender_type": event["sender_type"],
                "sender_id": event["sender_id"],
                "sender_name": event["sender_name"],
            }
        }))

    @database_sync_to_async
    def save_message(self, message, sender_type, sender_id, file_url):
        room = Room.objects.get(room_name=self.room_name)

        if sender_type == "client":
            sender_model = Client
        elif sender_type == "lawyer":
            sender_model = Lawyer
        else:
            raise ValueError("Invalid sender_type")

        try:
            sender_instance = sender_model.objects.get(id=sender_id)
        except sender_model.DoesNotExist:
            # Could log or handle differently
            sender_instance = None

        content_type = ContentType.objects.get_for_model(sender_instance) if sender_instance else None

        msg = Message.objects.create(
            room=room,
            message=message,
            sender_content_type=content_type,
            sender_object_id=sender_instance.id if sender_instance else None,
            file=file_url
        )
        return msg

    @database_sync_to_async
    def save_file(self, file_data, file_name):
        format, file_str = file_data.split(';base64,')
        decoded_file = base64.b64decode(file_str)

        safe_name = os.path.basename(file_name)
        unique_name = f"{uuid.uuid4().hex}_{safe_name}"

        path = os.path.join('uploads', unique_name)
        full_path = os.path.join(settings.MEDIA_ROOT, path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        with open(full_path, 'wb') as f:
            f.write(decoded_file)

        # Ensure URL uses forward slashes
        return f"{settings.MEDIA_URL}{path.replace(os.sep, '/')}"  

    @database_sync_to_async
    def get_sender_name(self, sender_type, sender_id):
        try:
            if sender_type == "client":
                return Client.objects.get(id=sender_id).first_name
            elif sender_type == "lawyer":
                return Lawyer.objects.get(id=sender_id).username
        except (Client.DoesNotExist, Lawyer.DoesNotExist):
            return "Unknown"
        return "Unknown"
