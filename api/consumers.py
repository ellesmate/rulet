import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .serializers import OrderSerializer


class CookConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.entity_name = self.scope['url_route']['kwargs']['entity']
        # self.room_group_name = 'chat_%s' % self.room_name
        self.entity_kitchen_name = f'kitchen_{self.entity_name}'

        # Join room group
        await self.channel_layer.group_add(
            self.entity_kitchen_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.entity_kitchen_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
    
    async def new_order(self, event):
        order = event['order']

        await self.send(text_data=json.dumps({
            'order': order
        }))

