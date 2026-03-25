from django.contrib import admin
from .models import Pizza, Topping, Drink, Order, OrderItem

admin.site.register(Pizza)
admin.site.register(Topping)
admin.site.register(Drink)
admin.site.register(Order)
admin.site.register(OrderItem)