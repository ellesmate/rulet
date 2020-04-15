from rest_framework import serializers
from .models import Waiter, Cashier, Chef, Order, Customer, MenuItem, Foundation, Category


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


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
