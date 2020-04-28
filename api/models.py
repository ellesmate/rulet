from django.db import models  # TODO: SqlLite to PostgreSQL
from django.core.validators import MinValueValidator

from account.models import Account


class Region(models.Model):
    name = models.CharField(max_length=40)


class Address(models.Model):
    street_name = models.CharField(max_length=40)
    street_number = models.CharField(max_length=20)
    zipcode = models.IntegerField()
    town = models.CharField(max_length=40)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)


class Efficiency(models.Model):
    efficiency_rate = models.FloatField()


class Entity(models.Model):
    name = models.CharField(max_length=60)
    image = models.ImageField()
    address = models.CharField(max_length=60)
    phone = models.CharField(max_length=12)
    rate = models.FloatField()

    def __str__(self):
        return f'{self.name} at {self.address}'


class Category(models.Model):
    name = models.CharField(max_length=30)
    image = models.ImageField()
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name


class MenuItem(models.Model):
    item_type = models.CharField(max_length=30)
    price = models.IntegerField()
    available = models.BooleanField()
    item_description = models.TextField()
    image = models.ImageField()
    size = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE)

    def __str__(self):
        return self.item_type


# class DrinkItem(MenuItem):
#     drink_type = models.CharField(max_length=30)
#     size = models.IntegerField()


# class FoodItem(MenuItem):
#     food_type = models.CharField(max_length=30)
#     calories = models.IntegerField()
#     weight = models.IntegerField()


class Customer(Account):
    pass


class Order(models.Model):
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, blank=True, null=True, on_delete=models.SET_NULL)
    time = models.DateTimeField(auto_now_add=True)
    # order_items = models.ManyToManyField(OrderItem)
    take_out = models.BooleanField()


class OrderItem(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    amount = models.IntegerField(validators=[MinValueValidator])
    order = models.ForeignKey(Order, on_delete=models.CASCADE)


class Employee(models.Model):
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    address = models.OneToOneField(Address, on_delete=models.CASCADE)
    efficiency = models.OneToOneField(Efficiency, on_delete=models.CASCADE)
    department = models.CharField(max_length=80)    # TODO: different object
    position = models.CharField(max_length=80)


class Chef(Employee):
    specialty = models.CharField(max_length=50)
    occupied = models.BooleanField()
    current_order = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL)


class Cashier(Employee):
    terminalNo = models.IntegerField()
    sessionNo = models.IntegerField()


class Waiter(Cashier):
    field = models.CharField(max_length=30)
    currently_serving = models.BooleanField()


class Manager(Employee):
    pass


class Supervisor(Employee):
    pass


