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


class Customer(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE, primary_key=True)


class Employee(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE, primary_key=True)
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    # email = models.EmailField()
    address = models.OneToOneField(Address, on_delete=models.CASCADE, null=True, blank=True)
    efficiency = models.OneToOneField(Efficiency, on_delete=models.CASCADE, null=True, blank=True)
    department = models.CharField(max_length=80, blank=True)    # TODO: different object
    position = models.CharField(max_length=80, blank=True)

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'


class Chef(models.Model):
    # employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, primary_key=True)
    specialty = models.CharField(max_length=50, blank=True)
    occupied = models.BooleanField(default=False)
    # current_order = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL)
    def __str__(self):
        return str(self.employee) + " Chef"


class Cashier(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, primary_key=True)
    terminalNo = models.IntegerField()
    sessionNo = models.IntegerField()

    def __str__(self):
        return str(self.employee) + " Cashier"


class Waiter(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, primary_key=True)
    field = models.CharField(max_length=30, blank=True)
    currently_serving = models.BooleanField(default=False)
    shift = models.BooleanField(default=False)

    # def __str__(self):
    #     return str(self.employee) + " Waiter"

class Courier(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, primary_key=True)
    shift = models.BooleanField(default=False)
    is_delivering = models.BooleanField(default=False)

    def __str__(self):
        return str(self.employee) + " Courier"


class Order(models.Model):
    NEW = 'NEW'
    COOKING = 'COO'
    DELIVERING = 'DEL'
    DONE = 'DON'
    ORDER_STATES_CHOICES = (
        (NEW, 'NEW'),
        (COOKING, 'COOKING'),
        (DELIVERING, 'DELIVERING'),
        (DONE, 'DONE'),
    )

    entity = models.ForeignKey(Entity, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, blank=True, null=True, on_delete=models.SET_NULL)
    time = models.DateTimeField(auto_now_add=True)
    # order_items = models.ManyToManyField(OrderItem)
    take_out = models.BooleanField()
    waiter = models.ForeignKey(Waiter, null=True, on_delete=models.SET_NULL)
    address = models.CharField(max_length=80, blank=True)

    status = models.CharField(
        max_length=3,
        choices=ORDER_STATES_CHOICES,
        default=NEW
    )


class OrderItem(models.Model):
    NEW = 'NEW'
    COOKING = 'COO'
    DELIVERING = 'DEL'
    DONE = 'DON'
    ORDER_ITEM_STATES_CHOICES = (
        (NEW, 'NEW'),
        (COOKING, 'COOKING'),
        (DELIVERING, 'DELIVERING'),
        (DONE, 'DONE'),
    )
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    cook = models.ForeignKey(Chef, blank=True, null=True, on_delete=models.SET_NULL)
    amount = models.IntegerField(validators=[MinValueValidator])
    wishes = models.CharField(max_length=200, blank=True)
    status = models.CharField(
        max_length=3,
        choices=ORDER_ITEM_STATES_CHOICES,
        default=NEW
    )

    def __str__(self):
        return f'{self.menu_item} | Status:{self.status}'




class Manager(Employee):
    pass


class Supervisor(Employee):
    pass


