from django.contrib import admin

# from .models import Place, Restaurant, Product, Ingredient, Employee, Order
from .models import Waiter, Cashier, Chef, Order, Customer, Entity, Category, MenuItem, OrderItem, Employee


admin.site.register(Waiter)
admin.site.register(Employee)
admin.site.register(Cashier)
admin.site.register(Chef)
admin.site.register(Order)
admin.site.register(Customer)
admin.site.register(MenuItem)
# admin.site.register(FoodItem)
# admin.site.register(DrinkItem)
admin.site.register(Entity)
admin.site.register(Category)
admin.site.register(OrderItem)


# class IngredientInline(admin.StackedInline):
#     model = Ingredient
#     extra = 3
#
#
# class ProductAdmin(admin.ModelAdmin):
#     inlines = [IngredientInline]
#
#
# admin.site.register(Place)
# admin.site.register(Restaurant)
# admin.site.register(Product, ProductAdmin)
# admin.site.register(Employee)
# admin.site.register(Order)
