from django.contrib import admin

from .models import Place, Restaurant, Product, Ingredient, Employee, Order


class IngredientInline(admin.StackedInline):
    model = Ingredient
    extra = 3


class ProductAdmin(admin.ModelAdmin):
    inlines = [IngredientInline]


admin.site.register(Place)
admin.site.register(Restaurant)
admin.site.register(Product, ProductAdmin)
admin.site.register(Employee)
admin.site.register(Order)
