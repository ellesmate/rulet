import channels.layers
from rest_framework import serializers
from asgiref.sync import async_to_sync


from .models import Waiter, Cashier, Chef, Order, Customer, MenuItem, Entity, Category, OrderItem


class EntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'

# class FoodItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = FoodItem
#         fields = '__all__'


# class DrinkItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DrinkItem
#         fields = '__all__'


class WaiterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Waiter
        fields = '__all__'


class CashierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cashier
        fields = '__all__'


class ChefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chef
        fields = '__all__'

# class OrderItemListSerializer(serializers.ListSerializer):
#     def create(self, validated_data):
#         ret = []

#         for data in validated_data:
#             ret.append(self.child.create(data))
#         return ret

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        # list_serializer_class = OrderItemListSerializer
        model = OrderItem
        fields = '__all__'


class CreateOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('menu_item', 'amount', 'wishes')


class OrderSerializer(serializers.ModelSerializer):
    orderitem_set = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = '__all__'
    

class CreateOrderSerializer(serializers.ModelSerializer):
    # order_items = serializers.PrimaryKeyRelatedField(many=True, queryset=OrderItem.objects.all())
    orderitem_set = CreateOrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        orderitem_validated_data = validated_data.pop('orderitem_set')
        order = Order.objects.create(**validated_data)
        orderitem_set_serializer = self.fields['orderitem_set']
        for each in orderitem_validated_data:
            each['order'] = order
        orderitems = orderitem_set_serializer.create(orderitem_validated_data)

        channel_layer = channels.layers.get_channel_layer()

        serializer = OrderSerializer(order)

        entity_name = order.entity.id
        async_to_sync(channel_layer.group_send)(
            f'kitchen_{entity_name}', 
            {
                'type': 'new_order',
                'order': serializer.data
            }
        )

        return order

    

# class OrderSerializer(serializers.ModelSerializer):
#     # order_items = serializers.PrimaryKeyRelatedField(many=True, queryset=OrderItem.objects.all())
#     order_items = OrderItemSerializer(many=True)
#     # menu_items = serializers.DjangoModelField()
#     # menu_items = serializers.SerializerMethodField()

#     class Meta:
#         model = Order
#         fields = '__all__'
