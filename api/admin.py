from django.contrib import admin

# from .models import Place, Restaurant, Product, Ingredient, Employee, Order
from .models import Waiter, Cashier, Chef, Order, Customer, Entity, Category, MenuItem, OrderItem, Employee


admin.site.register(Waiter)
admin.site.register(Employee)
admin.site.register(Cashier)
admin.site.register(Chef)
# admin.site.register(Order)
admin.site.register(Customer)
admin.site.register(MenuItem)
# admin.site.register(FoodItem)
# admin.site.register(DrinkItem)
admin.site.register(Entity)
admin.site.register(Category)
# admin.site.register(OrderItem)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Relations', {'fields': ['entity', 'customer', 'waiter']}),
        ('Order info', {'fields': ['address', 'take_out', 'status']})
    ]
    inlines = [OrderItemInline]

    
admin.site.register(Order, OrderAdmin)
