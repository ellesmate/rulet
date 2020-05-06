import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .serializers import OrderSerializer
from api import models


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
        print(text_data_json)
        update = text_data_json['update']

        print("RECEIVING")
        if not update.get('order_item_id') or not update.get('order_id') or not update.get('cook') or not update.get('status'):
            return
        
        order_item_id = update['order_item_id']
        order_id = update['order_id']
        cook_id = update['cook']
        status = update['status']

        print("DESERIALIZED")

        order_item = await sync_to_async(models.OrderItem.objects.get)(pk=order_item_id)
        # if (order_item.order != order):
        order_item.status = status
        order_item.cook = await sync_to_async(models.Chef.objects.get)(pk=cook_id)
        # order_item.save()

        print("OK. Sending")

        # Send message to room group
        await self.channel_layer.group_send(
            self.entity_kitchen_name,
            {
                'type': 'update_message',
                'update': update
            }
        )

    # Receive message from room group
    async def update_message(self, event):
        update = event['update']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'update': update
        }))
    
    async def new_order(self, event):
        order = event['order']

        await self.send(text_data=json.dumps({
            'order': order
        }))

