import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .serializers import OrderSerializer
from api import models


class WaiterConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.entity_name = self.scope['url_route']['kwargs']['entity']
        self.entity_hall_name = f'hall_{self.entity_name}'
        self.user = self.scope['user']
        
        if user.is_anonymous:
            await self.close()
            return

        await self.channel_layer.group_add(
            self.entity_hall_name,
            self.channel_name
        )

        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.entity_hall_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        await self.channel_layer.group_send(
            self.entity_hall_name,
            {
                'type': 'notify_waiter',
                'update': text_data_json
            }
        )

    async def notify_waiter(self, event):
        waiter = event['waiter']
        order_item = event['order_item']

        if self.user == waiter:
            await self.send(text_data=json.dumps({
                'order_item': order_item
            }))


class CookConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print(self.scope['user'])
        self.user = self.scope['user']

        if self.user.is_anonymous:
            await self.close()
            return

        print(dir(self.user))

        await self.get_basic_user_info()

        print(self.employee)
        print(self.entity)
        print(self.chef)
        

        self.entity_kitchen_name = f'kitchen_1'
        print(self.scope['user'])

        # Join room group
        await self.channel_layer.group_add(
            self.entity_kitchen_name,
            self.channel_name
        )

        await self.accept()
    
    @database_sync_to_async
    def get_basic_user_info(self):
        self.employee = self.user.employee
        self.entity = self.employee.entity
        self.chef = self.employee.chef

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.entity_kitchen_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive_json(self, content):
        update = content['update']

        order, order_item = await self.verify_received_data(update)

        if not order.take_out and order_item.status == 'DEL':
            order_item, waiter = await self.allocate_waiter(order_item)
            await self.channel_layer.group_send(
                f'hall_{self.entity.id}',
                {
                    'type': 'notify_waiter',
                    'order_item': order_item,
                    'waiter': waiter
                }
            )
        elif order.take_out and order.status == 'DEL':
            await self.channel_layer.group_send(
                f'delivery_{self.entity_name}',
                {
                    'type': 'new_order',
                    'update': order_item
                }
            )

        await self.channel_layer.group_send(
            self.entity_kitchen_name,
            {
                'type': 'update_message',
                'update': update
            }
        )
    
    @database_sync_to_async
    def verify_received_data(self, update):
        order_item_id = update.get('order_item_id')
        order_id = update.get('order_id')
        cook_id = update.get('cook')
        status = update.get('status')

        if not order_id or not order_item_id or not cook_id or not status:
            return None, None

        order_item = models.OrderItem.objects.get(pk=order_item_id)
        order = order_item.order

        order_item.status = status
        cook = models.Chef.objects.get(pk=cook_id)

        if self.chef != cook or order.id != order_id:
            return None, None

        order_item.cook = cook
        order_item.save()

        return order, order_item

    
    @database_sync_to_async
    def allocate_waiter(self, order_item):
        entity = order_item.entity

        order = order_item.order

        if order.waiter is not None:
            waiters = models.Waiter.objects.filter(account__entity=entity, shift=True)
            
            lucky = waiters[0]
            orders_num = len(lucky.order_set)
            for waiter in waiters:
                num = len(waiter.order_set)
                if orders_num > num:
                    lucky = waiter
                    orders_num = num
            
            order.waiter = lucky
            order.save()
        
        return order_item, self.user

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


# class CourierConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.user = 
#         self.entity_name = self.scope['url_route']['kwargs']['entity']
#         self.entity_hall_name = f'delivery_{self.entity_name}'

#         await self.channel_layer.group_add(
#             self.entity_delivery_name,
#             self.channel_name
#         )

#         await self.accept()
    
#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             self.entity_delivery_name,
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)

#         await self.channel_layer.group_send(
#             self.entity_delivery_name,
#             {
#                 'type': 'notify_waiter',
#                 'update': text_data_json
#             }
#         )

#     # async def notify_waiter(self, event):
#     #     update = event['update']

#     #     # Send message to WebSocket
#     #     await self.send(text_data=json.dumps({
#     #         'update': update
#     #     }))
    
#     async def new_order(self, event):
#         order = event['event']
#         models.Courier.objects.filter(account__entity=order.entity, shift=True, is_delivering=False)
