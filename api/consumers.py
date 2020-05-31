import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .serializers import OrderSerializer, WaiterSerializer
from api import models


class WaiterConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print(self.scope['user'])
        self.user = self.scope['user']

        if self.user.is_anonymous:
            await self.close()
            return

        await self.get_basic_user_info()

        # self.entity_hall_name = f'hall_{self.entity.id}'
        self.entity_hall_name = f'hall_{self.entity.pk}'

        await self.channel_layer.group_add(
            self.entity_hall_name,
            self.channel_name
        )

        await self.accept()

    @database_sync_to_async
    def get_basic_user_info(self):
        self.employee = self.user.employee
        self.entity = self.employee.entity
        self.waiter = self.employee.waiter
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.entity_hall_name,
            self.channel_name
        )

    async def receive(self, text_data):
        content = json.loads(text_data)
        print(content)

        if content.get('delivered') is not None:
            order_item = content['delivered']
            print(order_item)
            await self.change_order_item_status(order_item)
        elif content.get('payed') is not None:
            order = content['payed']
            await self.change_order_status(order)

        await self.send(text_data=text_data)

        # await self.channel_layer.group_send(
        #     self.entity_hall_name,
        #     {
        #         'type': 'notify_waiter',
        #         'update': text_data_json
        #     }
        # )

    @database_sync_to_async
    def change_order_item_status(self, order_item):
        db_order_item = models.OrderItem.objects.get(pk = order_item['id'])
        if db_order_item.order.waiter == self.waiter:
            db_order_item.status = order_item['status']
            db_order_item.save()
    
    @database_sync_to_async
    def change_order_status(self, order):
        db_order = models.Order.objects.get(pk = order['id'])
        if db_order.waiter == self.waiter:
            db_order.status = order['status']
            db_order.save()

    async def notify_waiter(self, event):

        waiter = event['waiter']
        order = event['order']

        if self.waiter.pk == waiter['employee']:
            await self.send(text_data=json.dumps({
                'order': order
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
        

        self.entity_kitchen_name = f'kitchen_{self.entity.pk}'
        print(self.scope['user'])

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
        await self.channel_layer.group_discard(
            self.entity_kitchen_name,
            self.channel_name
        )

    async def receive(self, text_data):
        content = json.loads(text_data)
        update = content['update']

        print(update)

        order, order_item = await self.verify_received_data(update)

        if not order.take_out and order_item.status == 'DEL':
            order_serializer, waiter_serializer = await self.allocate_waiter(order_item, order)
            await self.channel_layer.group_send(
                f'hall_{self.entity.pk}',
                {
                    'type': 'notify_waiter',
                    'order': order_serializer,
                    'waiter': waiter_serializer
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
    def allocate_waiter(self, order_item, order):
        entity = order.entity


        if False and order.waiter is None:
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

        serializer = OrderSerializer(order)
        waiter_serializer = WaiterSerializer(order.waiter)
        
        return serializer.data, waiter_serializer.data

    async def update_message(self, event):
        update = event['update']

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
