import json
from channels.generic.websocket import AsyncWebsocketConsumer


class VideoChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get room_name dynamically from the URL
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'video_chat_{self.room_name}'

        # Add this user to the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # Optional: notify others in the room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_status',
                'message': f"User {self.channel_name[:8]} joined.",
                'sender': self.channel_name
            }
        )

        print(f"[CONNECTED] {self.channel_name[:8]} joined room: {self.room_name}")

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_status',
                'message': f"User {self.channel_name[:8]} left.",
                'sender': self.channel_name
            }
        )

        print(f"[DISCONNECTED] {self.channel_name[:8]} left room: {self.room_name}")

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            print(f"Invalid JSON received: {text_data}")
            return

        msg_type = data.get('type')

        if msg_type in ['offer', 'answer', 'ice-candidate']:
            internal_type = msg_type.replace('-', '_')  # e.g., 'ice-candidate' → 'ice_candidate'
            data.pop('type', None)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': internal_type,
                    'sender': self.channel_name,
                    **data
                }
            )

            print(f"[SIGNAL] {msg_type} from {self.channel_name[:8]} broadcasted.")
        else:
            print(f"Unknown message type: {msg_type}")

    # --- Signal Handlers ---

    async def offer(self, event):
        if event['sender'] != self.channel_name:
            await self.send(json.dumps({
                'type': 'offer',
                'sdp': event['sdp'],
                'sender': event['sender']
            }))

    async def answer(self, event):
        if event['sender'] != self.channel_name:
            await self.send(json.dumps({
                'type': 'answer',
                'sdp': event['sdp'],
                'sender': event['sender']
            }))

    async def ice_candidate(self, event):
        if event['sender'] != self.channel_name:
            await self.send(json.dumps({
                'type': 'ice-candidate',
                'candidate': event['candidate'],
                'sender': event['sender']
            }))

    async def user_status(self, event):
        if event['sender'] != self.channel_name:
            await self.send(json.dumps({
                'type': 'user_status',
                'message': event['message'],
                'sender': event['sender']
            }))
