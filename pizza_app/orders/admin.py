from django.contrib import admin
from .models import Pizza, Topping, Drink, Order, OrderItem, Coupon, Location


@admin.register(Pizza)
class PizzaAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_small', 'price_medium', 'price_large', 'emoji')
    search_fields = ('name', 'description')
    filter_horizontal = ('available_toppings',)


@admin.register(Topping)
class ToppingAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_small', 'price_medium', 'price_large')
    search_fields = ('name',)


@admin.register(Drink)
class DrinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'emoji')
    search_fields = ('name',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date', 'status', 'total_price', 'coupon_code', 'discount_amount')
    list_filter = ('status',)
    search_fields = ('user__username', 'delivery_address', 'coupon_code')
    list_editable = ('status',)
    readonly_fields = ('date',)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'pizza', 'drink', 'quantity', 'size')
    list_filter = ('size',)


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percent', 'active')
    list_editable = ('active',)
    search_fields = ('code',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'phone', 'opening_hours')
    search_fields = ('name', 'city', 'address')
