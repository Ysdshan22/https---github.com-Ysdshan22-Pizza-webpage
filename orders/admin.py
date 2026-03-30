from django.contrib import admin
from .models import Location, Category, MenuItem, Allergen, Order, OrderItem

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'discount_percent', 'is_available']
    list_filter = ['category', 'is_available']
    filter_horizontal = ['allergens']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order']

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['city', 'address', 'phone']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total', 'created_at']

admin.site.register(Allergen)
admin.site.register(OrderItem)