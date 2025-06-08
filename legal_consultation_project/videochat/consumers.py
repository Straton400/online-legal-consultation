from channels.generic.websocket import AsyncWebsocketConsumer
import json

class VideoCallConsumer(AsyncWebsocketConsumer):
    participants = {}

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'videocall_{self.room_name}'

        if self.room_group_name not in VideoCallConsumer.participants:
            VideoCallConsumer.participants[self.room_group_name] = []

        VideoCallConsumer.participants[self.room_group_name].append(self.channel_name)
        is_initiator = len(VideoCallConsumer.participants[self.room_group_name]) == 1

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # Notify the frontend who is the initiator
        await self.send(text_data=json.dumps({
            "type": "join",
            "isInitiator": is_initiator
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        if self.room_group_name in VideoCallConsumer.participants:
            VideoCallConsumer.participants[self.room_group_name].remove(self.channel_name)

    async def receive(self, text_data):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'signal_message',
                'message': text_data,
                'sender_channel_name': self.channel_name
            }
        )

    async def signal_message(self, event):
        if self.channel_name != event['sender_channel_name']:
            await self.send(text_data=event['message'])
