from django.contrib import admin
from .models import Pizza, Topping, Drink, Order, OrderItem


@admin.register(Pizza)
class PizzaAdmin(admin.ModelAdmin):
    filter_horizontal = ('available_toppings',)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    filter_horizontal = ('toppings',)


admin.site.register(Topping)
admin.site.register(Drink)
admin.site.register(Order)