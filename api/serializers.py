from rest_framework import serializers
from .models import Waiter, Cashier, Chef, Order, Customer, MenuItem, Foundation, Category, OrderItem


class FoundationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Foundation
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

class OrderItemListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        ret = []

        for data in validated_data:
            ret.append(self.child.create(data))
        return ret

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        # list_serializer_class = OrderItemListSerializer
        model = OrderItem
        fields = ('amount', 'menu_item')

    # def to_representation(self, instance):
    #     return {
    #         'id': instance.id,
    #         'amount': instance.amount,
    #         'menu_item': instance.menu_item,
    #     }
    
    # def to_internal_value(self, data):
    #     amount = data.get['amount']
    #     menu_item = data.get['menu_item']

    #     if not amount:
    #         raise serializers.ValidationError({
    #             'amount': 'This field is required'
    #         })
    #     if not menu_item:
    #         raise serializers.ValidationError({
    #             'menu_item': 'This field is required'
    #         })
        
    #     return {
    #         'amount': amount,
    #         'menu_item': menu_item,
    #     }






class OrderSerializer(serializers.ModelSerializer):
    # order_items = serializers.PrimaryKeyRelatedField(many=True, queryset=OrderItem.objects.all())
    orderitem_set = OrderItemSerializer(many=True)
    # menu_items = serializers.DjangoModelField()
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
        return order
    
    # menu_items = serializers.SerializerMethodField()

    

# class OrderSerializer(serializers.ModelSerializer):
#     # order_items = serializers.PrimaryKeyRelatedField(many=True, queryset=OrderItem.objects.all())
#     order_items = OrderItemSerializer(many=True)
#     # menu_items = serializers.DjangoModelField()
#     # menu_items = serializers.SerializerMethodField()

#     class Meta:
#         model = Order
#         fields = '__all__'
