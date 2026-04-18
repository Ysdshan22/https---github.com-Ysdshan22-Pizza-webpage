from django.contrib import admin
from .models import Pizza, Side, Topping, Drink, Order, OrderItem

@admin.register(Pizza)
class PizzaAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price_small', 'price_medium', 'price_large', 'can_be_vegetarian', 'can_be_vegan')
    list_filter = ('category', 'can_be_vegetarian', 'can_be_vegan')
    search_fields = ('name',)

@admin.register(Side)
class SideAdmin(admin.ModelAdmin):
    list_display = ('name', 'side_type', 'price')

@admin.register(Topping)
class ToppingAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_small', 'price_medium', 'price_large')

@admin.register(Drink)
class DrinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'status', 'date')
    list_filter = ('status',)

admin.site.register(OrderItem)